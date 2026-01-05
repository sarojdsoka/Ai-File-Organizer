# 🚀 Quick Start Guide

## 🎯 Get Started in 3 Steps

### 1. Run Interactive Mode

```bash
cd ~/Projects/Dev/ai-file-organizer
./organizer.sh --interactive
```

### 2. Choose Action

- **Option 1** → Organize files
- **Option 2** → Analyze file system

### 3. Follow Prompts

Select AI provider, directory, and settings. Done!

## 📋 Quick Commands

```bash
# Interactive mode (Best!)
./organizer.sh --interactive

# Quick dry run
./organizer.sh --dry-run

# Execute organization
./organizer.sh --execute

# With AI provider
./organizer.sh --dry-run --ai groq

# Setup AI keys
./organizer.sh --setup

# Help
./organizer.sh --help
```

## 🤖 AI Provider Setup

### Groq (Recommended)
```bash
# Get key: https://console.groq.com/keys
echo 'export GROQ_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

### No AI (Fastest)
No setup needed! Just use `--ai none` or default.

## 📁 What Each Mode Does

### 📁 Organize Mode
- Scans directory recursively
- Categorizes files by type
- Moves files to organized folders
- Safe dry-run preview available

### 🔍 Analyze Mode
- Scans entire directory structure
- Shows categories breakdown
- Lists largest files/directories
- Finds old files (not modified in X days)
- Provides AI insights and cleanup tips

## 💡 Tips

- Always use **dry-run** first
- Start with **Downloads** folder
- Use **AI provider** for better insights
- Run **analysis** regularly (monthly)
- Check **old files** quarterly

## ⚡ Common Workflows

### Organize Downloads
```bash
./organizer.sh --dry-run --dir ~/Downloads
# Preview, then:
./organizer.sh --execute --dir ~/Downloads
```

### Analyze Home with AI
```bash
./organizer.sh --interactive
# Choose 2 (Analyze), then Groq
```

### Find Large Files
```bash
./organizer.sh --interactive
# Choose 2 (Analyze), set Top to 20
```

### Cleanup Old Files
```bash
./organizer.sh --interactive
# Choose 2 (Analyze), set Old to 30 days
```

## 🎯 File Categories

Files are organized into:
- **Documents** - PDF, DOC, TXT, MD
- **Images** - JPG, PNG, GIF, SVG
- **Videos** - MP4, MKV, AVI
- **Audio** - MP3, WAV, FLAC
- **Code** - PY, JS, JAVA, C++
- **Archives** - ZIP, RAR, TAR
- **Data** - CSV, XLS, SQL
- **Executables** - EXE, DEB, RPM

## 🔒 Safety

- ✅ Preview with dry-run
- ✅ No file overwrites
- ✅ Skips hidden files
- ✅ Preserves system folders
- ✅ Confirm before action

## ❓ Need Help?

```bash
./organizer.sh --help
```

Or see full documentation: `README.md`

## 📄 License

**MIT License** - Free to use, modify, and distribute!

---

**Happy Organizing! 🎉**  
**License**: MIT | **Version**: 2.0
