# Quick Start Guide

## 🚀 Getting Started

### 1. Rename Directory (Recommended)

**Current**: `Watchdog`  
**New**: `Export_File_Watchdog`

```powershell
# From parent directory (02_ETL_Scripts)
Rename-Item -Path "Watchdog" -NewName "Export_File_Watchdog"
```

### 2. Initialize Git (Already Done ✅)

```bash
git status  # Verify files are tracked
```

### 3. Create Initial Commit

```bash
git commit -m "Initial commit: Export File Watchdog Service v2.0.0"
```

### 4. Create GitHub Repository

**Option A: Via GitHub Website**
1. Go to github.com → New repository
2. Name: `Export_File_Watchdog`
3. Don't initialize with README
4. Copy the repository URL

**Option B: Via GitHub CLI**
```bash
gh repo create Export_File_Watchdog --public --source=. --remote=origin --push
```

### 5. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/Export_File_Watchdog.git
git branch -M main
git push -u origin main
```

## 📝 After Renaming Directory

Update these references:

1. **Task Scheduler** (`HPD Export Watchdog.xml`):
   - Update path in Task Scheduler GUI
   - Or edit XML file directly

2. **Directory Opus Buttons**:
   - Update command paths to use `Export_File_Watchdog`

3. **Launcher Scripts**:
   - Check if any have hardcoded paths (they should use absolute paths)

## ✅ Verification Checklist

- [ ] Directory renamed to `Export_File_Watchdog`
- [ ] Git repository initialized
- [ ] Initial commit created
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Task Scheduler updated (if using)
- [ ] Directory Opus buttons updated (if using)

## 📚 Documentation Files

- **README.md** - Main project documentation
- **CHANGELOG.md** - Version history
- **SUMMARY.md** - Project overview
- **GIT_SETUP.md** - Detailed Git/GitHub setup
- **docs/** - Additional documentation

---

**Ready to push to GitHub!** 🎉

