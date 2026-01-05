# 🤖 AI File Organizer & Analyzer

A smart, interactive tool for organizing files and analyzing your Linux file system with AI-powered insights.

## ✨ Features

- 📁 **Smart Organization** - Automatically categorize and organize files
- 🔍 **Deep Analysis** - Analyze disk usage, large files, and old files
- 🤖 **AI-Powered** - Get intelligent insights and cleanup suggestions
- 📊 **Visual Reports** - Beautiful ASCII charts and clear summaries
- 🎯 **Interactive Mode** - Easy-to-use guided interface
- ⚡ **Fast & Safe** - Dry run mode, no file loss risk

## 🚀 Quick Start

```bash
cd ~/Projects/Dev/ai-file-organizer
./organizer.sh --interactive
```

Follow the prompts to organize or analyze your files!

## 📖 Usage

### Interactive Mode (Recommended)

```bash
./organizer.sh --interactive
```

Choose what you want to do:
- **Option 1**: Organize files into folders
- **Option 2**: Analyze file system

### Quick Commands

```bash
# Preview organization
./organizer.sh --dry-run

# Actually organize files
./organizer.sh --execute

# With AI provider
./organizer.sh --dry-run --ai groq
```

## 🤖 AI Providers

| Provider | Description | Cost |
|----------|-------------|-------|
| **none** | No AI, fastest | Free |
| **groq** | Fast LLaMA 3 | Free tier |
| **openai** | GPT models | Paid |
| **anthropic** | Claude | Paid |
| **ollama** | Local models | Free |

### Setup AI Provider

```bash
# Groq (Recommended)
echo 'export GROQ_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc

# OpenAI
echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc

# Anthropic
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.zshrc
```

Get API keys:
- Groq: https://console.groq.com/keys
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys

## 📁 File Organization

Automatically organizes files into categories:

- **Documents** - PDF, DOC, TXT, MD
- **Images** - JPG, PNG, SVG, WEBP
- **Videos** - MP4, MKV, AVI, MOV
- **Audio** - MP3, WAV, FLAC
- **Code** - PY, JS, JAVA, CPP
- **Archives** - ZIP, RAR, TAR
- **Data** - CSV, XLS, SQL
- **Executables** - EXE, DEB, RPM

## 🔍 File System Analysis

Get insights about your storage:

### What It Shows

1. **Overview**
   - Total disk usage
   - File and directory counts
   - Dominant categories

2. **Categories Breakdown**
   - File type distribution
   - Size per category
   - Visual bar charts

3. **Largest Files**
   - Top N files by size
   - File paths and dates

4. **Largest Directories**
   - Top N directories
   - Storage hogs

5. **Old Files**
   - Files not modified in X days
   - Perfect for cleanup

6. **AI Insights**
   - Smart observations
   - Cleanup recommendations
   - Actionable tips

### Example Output

```
📊 FILE SYSTEM OVERVIEW
======================================================================
📁 Directory: /home/user
📦 Total Size: 4.5GB
📄 Files: 1,234
📂 Directories: 56

----------------------------------------------------------------------
📋 CATEGORIES BREAKDOWN
----------------------------------------------------------------------

Videos        2.3GB (  23 files)
            [██████████████████████████████████████████████████] 51.1%

Documents     1.5GB ( 156 files)
            [█████████████████████████████████████            ] 33.3%

Code          500MB (  89 files)
            [█████████████                                 ] 11.1%

----------------------------------------------------------------------
🤖 INSIGHTS
======================================================================
📊 AI-Powered Insights

🎯 Summary:
   Your file system shows good organization with Videos (51%) and 
   Documents (33%) dominating storage. Average file size is 3.7MB.

📈 Observations:
   • Videos category uses over half your storage space
   • 47 files haven't been modified in 90+ days
   • 23 video files average 100MB each

🧹 Recommendations:
   1. Review large video files in ~/Downloads/videos/
   2. Archive 47 old files (>90 days) to external storage
   3. Delete duplicate PDFs found in Documents/
   4. Compress old backups to save ~500MB

✅ Done!
======================================================================
```

## 🛡️ Safety Features

- **Dry Run Mode** - Preview before executing
- **No Overwrites** - Skips existing files
- **Hidden Files** - Safely ignores system files
- **Skip Dirs** - Avoids node_modules, .git, etc.

## 📂 Directories Analyzed

Organizes and analyzes:
- Home directory
- Desktop
- Downloads
- Documents
- Projects
- Custom paths

Skips:
- Hidden files/folders
- System directories (.cache, .config, .local)
- VCS folders (.git, .svn)
- Build artifacts (node_modules, __pycache__, venv)

## 🎯 Best Practices

1. **Always dry run first**
   ```bash
   ./organizer.sh --dry-run
   ```

2. **Start with specific folders**
   ```bash
   ./organizer.sh --dry-run --dir ~/Downloads
   ```

3. **Use AI for better insights**
   ```bash
   ./organizer.sh --interactive  # Choose AI provider
   ```

4. **Regular cleanup**
   - Run analysis monthly
   - Review old files quarterly
   - Archive rarely used data

## 🔧 Troubleshooting

**Permission denied**
```bash
chmod +x organizer.sh
```

**API key not found**
```bash
echo $GROQ_API_KEY  # Check if set
source ~/.zshrc       # Reload config
```

**Python not found**
```bash
sudo apt install python3
```

## 📁 Project Structure

```
ai-file-organizer/
├── organizer.py      # Main Python script
├── organizer.sh      # Bash wrapper
├── README.md         # This file
└── QUICK_START.md    # Quick reference
```

## 🤝 Contributing

Feel free to customize categories, add more AI providers, or improve features!

## 📄 License

Free to use and modify.

---

**Made with ❤️ for clean, organized file systems**

**Location**: `~/Projects/Dev/ai-file-organizer/`
