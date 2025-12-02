# Git and GitHub Setup Guide

## Directory Renaming

### Recommended New Name

**Current**: `Watchdog`  
**Recommended**: `Export_File_Watchdog`

This name is more descriptive and avoids confusion with other watchdog scripts (e.g., file chunking watchdog).

### Renaming Steps

1. **Stop the watchdog service** (if running):
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "launchers\stop_watchdog_service.ps1"
   ```

2. **Rename the directory**:
   ```powershell
   # From parent directory
   Rename-Item -Path "Watchdog" -NewName "Export_File_Watchdog"
   ```

3. **Update Task Scheduler** (if using auto-start):
   - Open Task Scheduler
   - Find "HPD Export Watchdog" task
   - Edit the action to point to new path:
     ```
     C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\watchdog_service.py
     ```

4. **Update Directory Opus buttons** (if configured):
   - Update all button commands to use new path:
     ```
     C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\...
     ```

5. **Update launcher scripts** (if they have hardcoded paths):
   - The launcher scripts use absolute paths, so they should still work
   - But verify they point to the correct location

## Git Repository Setup

### Initial Setup

1. **Initialize repository** (already done):
   ```bash
   git init
   ```

2. **Add all files**:
   ```bash
   git add .
   ```

3. **Create initial commit**:
   ```bash
   git commit -m "Initial commit: Export File Watchdog Service v2.0.0"
   ```

### GitHub Setup

1. **Create repository on GitHub**:
   - Go to GitHub.com
   - Click "New repository"
   - Name: `Export_File_Watchdog` (or your preferred name)
   - Description: "Automated file monitoring and organization service for export files"
   - Choose Public or Private
   - **Do NOT** initialize with README (we already have one)

2. **Add remote and push**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/Export_File_Watchdog.git
   git branch -M main
   git push -u origin main
   ```

### Alternative: Using GitHub CLI

```bash
gh repo create Export_File_Watchdog --public --source=. --remote=origin --push
```

## Git Workflow

### Making Changes

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

3. **Push to GitHub**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request** on GitHub

### Updating CHANGELOG

When making significant changes:
1. Update `CHANGELOG.md` with version number and changes
2. Commit the changelog update separately:
   ```bash
   git add CHANGELOG.md
   git commit -m "docs: Update CHANGELOG for v2.0.1"
   ```

## Ignored Files

The `.gitignore` file excludes:
- Python cache files (`__pycache__/`)
- Log files (`logs/*.log`)
- IDE configuration files
- OS-specific files
- Temporary files

## Branch Strategy

- **main**: Production-ready code
- **develop**: Development branch (optional)
- **feature/***: Feature branches
- **hotfix/***: Emergency fixes

## Commit Message Convention

Use descriptive commit messages:
- `feat: Add new export type support`
- `fix: Resolve file locking issue`
- `docs: Update README with new features`
- `refactor: Improve year extraction logic`
- `chore: Update dependencies`

## Tags for Releases

Tag releases for version tracking:

```bash
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

## Troubleshooting

### If you need to update remote URL:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/Export_File_Watchdog.git
```

### If you need to remove sensitive data:
```bash
# Use git filter-branch or BFG Repo-Cleaner
# Be careful - this rewrites history
```

### If launcher scripts need path updates:
All launcher scripts use absolute paths, so they should work after renaming. However, if you want to make them relative or update them:

1. Edit each launcher script
2. Update the path references
3. Commit the changes

---

**Note**: After renaming the directory, remember to update:
- Task Scheduler configuration
- Directory Opus button commands
- Any shortcuts or batch files that reference the old path

