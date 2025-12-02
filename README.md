# Export File Watchdog Service

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated file monitoring service that watches designated folders for export files and automatically organizes them into structured directories with year-based subfolders for time-series exports.

## 🎯 Features

- **Automated File Organization**: Monitors Desktop and Downloads folders for export files
- **Year-Based Organization**: Automatically extracts year from filenames and organizes into year subfolders
- **Robust File Handling**: Detects locked files (e.g., open in Excel) and retries with exponential backoff
- **Multiple Export Types**: Supports CAD exports, RMS exports, overtime reports, summons, and more
- **Silent Operation**: Runs hidden in the background with no taskbar entry
- **Rotating Logs**: Automatic log rotation (5MB max, 5 backup files)
- **Duplicate Detection**: Prevents multiple instances from running simultaneously
- **Dynamic Paths**: Uses `Path.home()` for portability across different user accounts

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Export Types](#export-types)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Windows OS (designed for Windows file system monitoring)
- Required Python packages:
  ```bash
  pip install watchdog
  ```

### Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure paths in `watchdog_service.py` if needed (defaults use `Path.home()`)
4. Set up Windows Task Scheduler (optional, for auto-start at logon)

## ⚡ Quick Start

### Manual Start

**Silent (Recommended):**
```powershell
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "launchers\start_watchdog_service_silent.ps1"
```

**With Confirmation:**
```powershell
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "launchers\start_watchdog_service.ps1"
```

**VBScript (Simplest):**
```cmd
wscript.exe launchers\start_watchdog_service.vbs
```

### Stop Service

```powershell
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "launchers\stop_watchdog_service.ps1"
```

## ⚙️ Configuration

### Monitored Folders

The service monitors these locations:
- `OneDrive - City of Hackensack\Desktop`
- `OneDrive - City of Hackensack\Downloads`
- `Downloads` (local)

### Destination

All organized files are moved to:
- `OneDrive - City of Hackensack\05_EXPORTS\`

## 📁 Export Types

### Legacy Exports (Timestamp Prefix)

- **SCRPA_CAD_Export** → `_CAD/SCRPA/`
- **SCRPA_RMS_Export** → `_RMS/SCRPA/`
- **OTActivity** → `_POSS_EXPORT/OVERTIME_EXPORT/`
- **TimeOffActivity** → `_POSS_EXPORT/TIME_OFF_EXPORT/`
- **e_ticket** → `_Summons/E_Ticket/`
- **Backtracet_Arrests_Export** → `_BACKTRACE_ARRESTS/`

### Time-Series Exports (Year-Based Organization)

#### Monthly Exports
- **Pattern**: `YYYY_MM_Monthly_CAD.xlsx` or `YYYY_MM_Monthly_RMS.xlsx`
- **Destination**: `_CAD/monthly_export/YYYY/` or `_RMS/monthly_export/YYYY/`
- **Example**: `2025_11_Monthly_CAD.xlsx` → `_CAD/monthly_export/2025/`

#### Rolling 13-Month Exports
- **Pattern**: `YYYY_MM_to_YYYY_MM_Rolling13_CAD.xlsx` (or `_RMS`)
- **Destination**: `_CAD/rolling_13/YYYY/` or `_RMS/rolling_13/YYYY/`
- **Example**: `2024_09_to_2025_09_Rolling13_RMS.xlsx` → `_RMS/rolling_13/2025/`

#### Response Time Exports
- **Pattern**: `YYYY_MM_to_YYYY_MM_ResponseTime_CAD.xlsx` (or `_RMS`)
- **Destination**: `_CAD/response_time/YYYY/` or `_RMS/response_time/YYYY/`
- **Example**: `2024_08_to_2025_08_ResponseTime_CAD.xlsx` → `_CAD/response_time/2025/`

## 📂 Directory Structure

```
Export_File_Watchdog/
├── watchdog_service.py          # Main service script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── SUMMARY.md                   # Project summary
├── .gitignore                   # Git ignore rules
│
├── launchers/                   # Launcher scripts
│   ├── start_watchdog_service.vbs
│   ├── start_watchdog_service.bat
│   ├── start_watchdog_service.ps1
│   ├── start_watchdog_service_silent.ps1
│   └── stop_watchdog_service.ps1
│
├── docs/                        # Documentation
│   ├── Directory_Opus_Setup.md
│   ├── Directory_Opus_Button_Config.md
│   └── Watchdog_Directory_Summary.md
│
├── logs/                        # Log files (auto-created)
│   └── watchdog_service.log
│
├── Data_Validation/             # Data validation scripts (empty)
│
├── Other_ETL_Scripts/           # Other ETL-related scripts (empty)
│
└── archive/                     # Archived files
    └── comprehensive_export_watchdog.py
```

## 💻 Usage

### Running as a Service

The service runs continuously in the background. It can be started:
- Manually via launcher scripts
- Automatically at Windows logon via Task Scheduler
- Via Directory Opus toolbar buttons

### Logging

Logs are automatically written to `logs/watchdog_service.log` with:
- Automatic rotation (5MB max file size)
- 5 backup files retained
- Timestamped entries for all operations

### File Processing

The service:
1. Monitors folders for new/modified files
2. Matches filenames against configured patterns
3. Extracts year information (for time-series exports)
4. Checks if file is locked (open in Excel, etc.)
5. Retries up to 5 times with 2-second delays
6. Moves file to appropriate destination with year subfolder
7. Logs all operations

## 📚 Documentation

- [Directory Opus Setup Guide](docs/Directory_Opus_Setup.md) - Configure Directory Opus buttons
- [Button Configuration](docs/Directory_Opus_Button_Config.md) - Detailed button setup
- [Project Summary](SUMMARY.md) - High-level overview

## 🔧 Development

### Requirements

```txt
watchdog>=3.0.0
```

### Code Structure

- **FileMover**: Handles file operations with lock detection and retry logic
- **YearExtractor**: Extracts year information from filenames using different strategies
- **ExportWatchdogHandler**: Main file system event handler
- **setup_logging**: Configures rotating file handler

### Adding New Export Types

Edit `watchdog_service.py` and add entries to either:
- `legacy_rules` dictionary (for timestamp-prefixed files)
- `new_rules` dictionary (for year-based organization)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [watchdog](https://github.com/gorakhargosh/watchdog) library
- Designed for City of Hackensack ETL workflows

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Version**: 2.0.0  
**Last Updated**: December 2024
