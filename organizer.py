#!/usr/bin/env python3
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import time


class AIManager:
    def __init__(self, ai_provider: str = "none"):
        self.ai_provider = ai_provider
        self.api_key = self.get_api_key()
        
    def get_api_key(self) -> str:
        if self.ai_provider == "none":
            return ""
        elif self.ai_provider == "groq":
            return os.getenv('GROQ_API_KEY', '')
        elif self.ai_provider == "openai":
            return os.getenv('OPENAI_API_KEY', '')
        elif self.ai_provider == "anthropic":
            return os.getenv('ANTHROPIC_API_KEY', '')
        return ""
    
    def call_ai(self, prompt: str, max_tokens: int = 50) -> str:
        if self.ai_provider == "groq":
            return self.call_groq_api(prompt, max_tokens)
        elif self.ai_provider == "openai":
            return self.call_openai_api(prompt, max_tokens)
        elif self.ai_provider == "anthropic":
            return self.call_anthropic_api(prompt, max_tokens)
        return ""
    
    def call_groq_api(self, prompt: str, max_tokens: int) -> str:
        try:
            import http.client
            conn = http.client.HTTPSConnection("api.groq.com")
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = json.dumps({
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            })
            conn.request("POST", "/openai/v1/chat/completions", data, headers)
            response = conn.getresponse()
            result = json.loads(response.read())
            return result['choices'][0]['message']['content'].strip()
        except:
            return ""
    
    def call_openai_api(self, prompt: str, max_tokens: int) -> str:
        try:
            import http.client
            conn = http.client.HTTPSConnection("api.openai.com")
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = json.dumps({
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            })
            conn.request("POST", "/v1/chat/completions", data, headers)
            response = conn.getresponse()
            result = json.loads(response.read())
            return result['choices'][0]['message']['content'].strip()
        except:
            return ""
    
    def call_anthropic_api(self, prompt: str, max_tokens: int) -> str:
        try:
            import http.client
            conn = http.client.HTTPSConnection("api.anthropic.com")
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01'
            }
            data = json.dumps({
                "model": "claude-3-haiku-20240307",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]
            })
            conn.request("POST", "/v1/messages", data, headers)
            response = conn.getresponse()
            result = json.loads(response.read())
            return result['content'][0]['text'].strip()
        except:
            return ""


CATEGORIES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.md', '.tex'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
    'Code': ['.py', '.js', '.java', '.c', '.cpp', '.h', '.php', '.rb', '.go', '.rs', '.sh', '.html', '.css', '.json', '.xml', '.yaml', '.yml'],
    'Data': ['.csv', '.xls', '.xlsx', '.sql', '.db', '.sqlite'],
    'Executables': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm', '.sh'],
}


class FileOrganizer(AIManager):
    def __init__(self, ai_provider: str = "none"):
        super().__init__(ai_provider)
        self.base_dir = Path.home()
        self.categories = CATEGORIES
    
    def scan_files(self, directory: Path) -> List[tuple]:
        files = []
        for item in directory.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                ext = item.suffix.lower()
                files.append((item, ext))
            elif item.is_dir() and not item.name.startswith('.'):
                if item.name not in {'node_modules', '.git', '__pycache__', 'venv', '.venv', 'build', 'dist', '.cache', '.config', '.local'}:
                    files.extend(self.scan_files(item))
        return files
    
    def get_category(self, ext: str) -> str:
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        return 'Other'
    
    def organize(self, dry_run: bool = False, verbose: bool = False):
        print(f"🔍 Scanning files in {self.base_dir}...")
        files = self.scan_files(self.base_dir)
        
        if not files:
            print("No files found to organize!")
            return
        
        print(f"📊 Found {len(files)} files")
        
        plan = {}
        for file_path, ext in files:
            category = self.get_category(ext)
            target_dir = self.base_dir / category
            
            if category not in plan:
                plan[category] = []
            plan[category].append((file_path, target_dir / file_path.name))
        
        print("\n📋 Organization Plan:")
        for category, moves in sorted(plan.items()):
            print(f"\n  {category}: {len(moves)} files")
            if verbose:
                for source, target in moves[:3]:
                    print(f"    {source.name} → {category}/")
                if len(moves) > 3:
                    print(f"    ... and {len(moves) - 3} more")
        
        if not dry_run:
            print("\n🚀 Organizing files...")
            moved_count = 0
            
            for category, moves in plan.items():
                target_dir = moves[0][1].parent
                target_dir.mkdir(exist_ok=True)
                
                for source, target in moves:
                    if not target.exists():
                        import shutil
                        shutil.move(str(source), str(target))
                        moved_count += 1
                        if verbose:
                            print(f"  ✓ {source.name} → {category}/")
                    elif verbose:
                        print(f"  ⚠ Skipped {source.name} (already exists)")
            
            print(f"\n✅ Done! Moved {moved_count} files")
        else:
            print("\n🔒 Dry run complete. Use --execute to actually move files.")


class FileSystemAnalyzer(AIManager):
    def __init__(self, ai_provider: str = "none"):
        super().__init__(ai_provider)
        self.base_dir = Path.home()
    
    def scan(self, directory: Path) -> Dict:
        files = []
        dirs = []
        total = 0
        
        for item in directory.iterdir():
            if item.name.startswith('.'):
                continue
            
            if item.is_file():
                try:
                    size = item.stat().st_size
                    files.append({'path': item, 'size': size, 'mtime': item.stat().st_mtime, 'ext': item.suffix.lower()})
                    total += size
                except:
                    pass
            elif item.is_dir():
                try:
                    dir_size = self.get_dir_size(item)
                    dirs.append({'path': item, 'size': dir_size})
                    total += dir_size
                except:
                    pass
        
        return {'files': files, 'dirs': dirs, 'total': total, 'file_count': len(files), 'dir_count': len(dirs)}
    
    def get_dir_size(self, directory: Path) -> int:
        total = 0
        for item in directory.rglob('*'):
            if item.is_file() and not item.name.startswith('.'):
                try:
                    total += item.stat().st_size
                except:
                    pass
        return int(total)
    
    def categorize_files(self, files: List[Dict]) -> Dict:
        categories = {cat: {'files': [], 'size': 0} for cat in list(CATEGORIES.keys()) + ['Other']}
        
        for file_info in files:
            ext = file_info['ext']
            categorized = False
            
            for category, extensions in CATEGORIES.items():
                if ext in extensions:
                    categories[category]['files'].append(file_info)
                    categories[category]['size'] += file_info['size']
                    categorized = True
                    break
            
            if not categorized:
                categories['Other']['files'].append(file_info)
                categories['Other']['size'] += file_info['size']
        
        return categories
    
    @staticmethod
    def format_size(size: int) -> str:
        current = float(size)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if current < 1024:
                return f"{current:.1f}{unit}"
            current /= 1024
        return f"{current:.1f}PB"
    
    @staticmethod
    def format_date(timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
    
    def display_overview(self, data: Dict, categories: Dict):
        print("\n" + "="*70)
        print("📊 FILE SYSTEM OVERVIEW")
        print("="*70)
        print(f"\n📁 Directory: {self.base_dir}")
        print(f"📦 Total Size: {self.format_size(data['total'])}")
        print(f"📄 Files: {data['file_count']:,}")
        print(f"📂 Directories: {data['dir_count']:,}")
        
        print("\n" + "-"*70)
        print("📋 CATEGORIES BREAKDOWN")
        print("-"*70)
        
        for category, info in sorted(categories.items(), key=lambda x: x[1]['size'], reverse=True):
            count = len(info['files'])
            size = self.format_size(info['size'])
            percentage = (info['size'] / data['total']) * 100 if data['total'] > 0 else 0
            bar = '█' * int(percentage / 2)
            
            print(f"\n{category:<12} {size:>8} ({count:4} files)")
            print(f"{'':<12} [{bar:<50}] {percentage:5.1f}%")
    
    def display_large_files(self, files: List[Dict], top_n: int = 10):
        large = sorted(files, key=lambda x: x['size'], reverse=True)[:top_n]
        
        print("\n" + "-"*70)
        print(f"🐘 TOP {top_n} LARGEST FILES")
        print("-"*70)
        
        for i, f in enumerate(large, 1):
            path = str(f['path'])
            if len(path) > 50:
                path = '...' + path[-47:]
            print(f"\n{i:2}. {path}")
            print(f"    Size: {self.format_size(f['size'])} | Modified: {self.format_date(f['mtime'])}")
    
    def display_old_files(self, files: List[Dict], days: int = 90, top_n: int = 10):
        cutoff = time.time() - (days * 86400)
        old = sorted([f for f in files if f['mtime'] < cutoff], key=lambda x: x['mtime'])[:top_n]
        
        print("\n" + "-"*70)
        print(f"📅 TOP {top_n} OLDEST FILES (Not modified in {days}+ days)")
        print("-"*70)
        
        if not old:
            print("\n  No old files found")
            return
        
        for i, f in enumerate(old, 1):
            path = str(f['path'])
            if len(path) > 50:
                path = '...' + path[-47:]
            print(f"\n{i:2}. {path}")
            print(f"    Size: {self.format_size(f['size'])} | Modified: {self.format_date(f['mtime'])}")
    
    def display_large_dirs(self, dirs: List[Dict], top_n: int = 10):
        large = sorted(dirs, key=lambda x: x['size'], reverse=True)[:top_n]
        
        print("\n" + "-"*70)
        print(f"📁 TOP {top_n} LARGEST DIRECTORIES")
        print("-"*70)
        
        for i, d in enumerate(large, 1):
            path = str(d['path'])
            if len(path) > 50:
                path = '...' + path[-47:]
            print(f"\n{i:2}. {path}")
            print(f"    Size: {self.format_size(d['size'])}")
    
    def generate_summary(self, data: Dict, categories: Dict, large_files: List[Dict]) -> str:
        if self.ai_provider == "none" or not self.api_key:
            return self._basic_summary(data, categories)
        
        try:
            top_cats = sorted(categories.items(), key=lambda x: x[1]['size'], reverse=True)[:5]
            prompt = f"""Analyze this file system:

Directory: {self.base_dir}
Total Size: {self.format_size(data['total'])}
Files: {data['file_count']:,}
Directories: {data['dir_count']:,}

Top Categories:
"""
            for cat, info in top_cats:
                prompt += f"  - {cat}: {len(info['files'])} files, {self.format_size(info['size'])}\n"
            
            prompt += """Provide:
1. Brief summary
2. 3-4 key observations
3. 3-4 cleanup recommendations
Keep it concise."""
            
            result = self.call_ai(prompt, 800)
            if result:
                return f"📊 AI-Powered Insights\n\n{result}"
        except:
            pass
        
        return self._basic_summary(data, categories)
    
    def _basic_summary(self, data: Dict, categories: Dict) -> str:
        largest = max(categories.items(), key=lambda x: x[1]['size'])
        return f"""📊 File System Summary

🎯 Overview:
   {data['file_count']:,} files, {data['dir_count']:,} directories
   Total: {self.format_size(data['total'])}

📈 Key Findings:
   • Largest: {largest[0]} ({self.format_size(largest[1]['size'])})
   • Avg file: {self.format_size(data['total'] / max(data['file_count'], 1))}

🧹 Suggestions:
   1. Review {largest[0]} - uses most space
   2. Check for duplicates
   3. Archive old files
   4. Consider external storage"""
    
    def analyze(self, top_n: int = 10, old_days: int = 90):
        print(f"🔍 Scanning {self.base_dir}...")
        
        data = self.scan(self.base_dir)
        categories = self.categorize_files(data['files'])
        
        self.display_overview(data, categories)
        self.display_large_dirs(data['dirs'], top_n)
        self.display_large_files(data['files'], top_n)
        self.display_old_files(data['files'], old_days, top_n)
        
        print("\n" + "="*70)
        print("🤖 INSIGHTS")
        print("="*70)
        print(self.generate_summary(data, categories, data['files'][:top_n]))
        
        print("\n" + "="*70)
        print("✅ Done!")
        print("="*70)


def list_providers():
    providers = {
        'none': 'No AI',
        'groq': 'Groq (Free tier)',
        'openai': 'OpenAI',
        'anthropic': 'Anthropic',
        'ollama': 'Ollama (Local)'
    }
    print("\n🤖 AI Providers:\n")
    for name, desc in providers.items():
        print(f"  {name:12} - {desc}")
    print()


def interactive():
    print("\n" + "="*60)
    print("🎯 AI File Organizer & Analyzer")
    print("="*60)
    
    print("\n🚀 Choose action:")
    print("  1. 📁 Organize files")
    print("  2. 🔍 Analyze file system")
    
    action = input("\nChoice (1-2, default: 2): ").strip() or "2"
    
    if action not in ['1', '2']:
        print("❌ Invalid")
        return
    
    print("\n🤖 AI Provider:")
    list_providers()
    provider = input("\nProvider (default: none): ").strip() or "none"
    
    print("\n📁 Directory:")
    print("  1. Home (~)")
    print("  2. Desktop")
    print("  3. Downloads")
    print("  4. Documents")
    print("  5. Projects")
    print("  6. Custom")
    
    choice = input("\nChoice (1-6, default: 1): ").strip() or "1"
    dirs = {
        '1': Path.home(),
        '2': Path.home() / 'Desktop',
        '3': Path.home() / 'Downloads',
        '4': Path.home() / 'Documents',
        '5': Path.home() / 'Projects',
        '6': Path(input("Path: ").strip())
    }
    directory = dirs.get(choice, Path.home())
    
    if action == '1':
        dry_run = input("\nDry run? (y/n, default: y): ").strip().lower() != 'n'
        
        print(f"\n⚙️  Organize: {directory}")
        print(f"    AI: {provider}")
        print(f"    Dry Run: {dry_run}")
        
        if input("\nProceed? (y/n): ").strip().lower() == 'y':
            print("\n" + "="*60)
            org = FileOrganizer(provider)
            org.base_dir = directory
            org.organize(dry_run, True)
            if dry_run:
                print("\n💡 Run without dry run to execute")
    
    elif action == '2':
        top_n = input("\nTop N items (default: 10): ").strip() or "10"
        old_days = input("Old files threshold days (default: 90): ").strip() or "90"
        
        try:
            top_n = int(top_n)
            old_days = int(old_days)
        except:
            top_n, old_days = 10, 90
        
        print(f"\n⚙️  Analyze: {directory}")
        print(f"    AI: {provider}")
        print(f"    Top: {top_n}, Old: {old_days} days")
        
        if input("\nProceed? (y/n): ").strip().lower() == 'y':
            print("\n" + "="*60)
            analyzer = FileSystemAnalyzer(provider)
            analyzer.base_dir = directory
            analyzer.analyze(top_n, old_days)
    
    print("\n" + "="*60)
    print("✅ Done!")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='🤖 AI File Organizer & Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Examples:\n  organizer --interactive\n  organizer --dry-run --ai groq\n  organizer --execute'
    )
    
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--ai', choices=['none', 'groq', 'openai', 'anthropic', 'ollama'], default='none')
    parser.add_argument('-d', '--directory', default=str(Path.home()))
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('-e', '--execute', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--list-ai', action='store_true')
    
    args = parser.parse_args()
    
    if args.list_ai:
        list_providers()
        return
    
    if args.interactive:
        interactive()
        return
    
    if not args.execute and not args.dry_run:
        args.dry_run = True
    
    org = FileOrganizer(args.ai)
    org.base_dir = Path(args.directory).expanduser()
    org.organize(args.dry_run, args.verbose)


if __name__ == '__main__':
    main()
