# Changelog

All notable changes to the Export File Watchdog Service will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.2] - 2024-12-02

### Added
- Support for LawSoft arrest exports (`YYYY_MM_LAWSOFT_ARREST.xlsx`) with year-based organization
- Support for generic Response Time exports (detects CAD/RMS from filename or defaults to CAD)
- Support for CSV format in e-ticket exports (previously only .xlsx)
- Support for .xls format in Overtime and TimeOff exports (in addition to .xlsx)
- Three new Benchmark export types:
  - `vehicle-pursuit-reports` → `Benchmark/vehicle_pursuit/`
  - `use-of-force-reports` → `Benchmark/use_force/`
  - `show-of-force-reports` → `Benchmark/show_force/`
- Overwrite mode for Benchmark reports (replaces existing files instead of timestamping)
- Automatic trailing number removal for Benchmark reports (removes `(1)`, `(02)`, etc. from filenames)

### Changed
- Updated Overtime export destination path from `_POSS_EXPORT/OVERTIME_EXPORT/` to `_Overtime/`
- Updated TimeOff export destination path from `_POSS_EXPORT/TIME_OFF_EXPORT/` to `_Time_Off/`
- Enhanced pattern matching to support both `ResponseTime` and `Response_Time` naming conventions
- Improved error handling in PowerShell launcher scripts to suppress red text errors in Directory Opus

### Fixed
- Directory Opus button configuration - fixed inline VBScript code requirement for Script Function type
- File format detection for legacy exports (now properly handles .xls, .xlsx, and .csv)

## [2.0.1] - 2024-12-XX

### Changed
- Renamed project directory from `Watchdog` to `Export_File_Watchdog` for better clarity and consistency
- Updated documentation to reflect new directory name
- Added `Data_Validation/` and `Other_ETL_Scripts/` directories to project structure

## [2.0.0] - 2024-12-01

### Added
- Complete refactoring with object-oriented design
- Dynamic path support using `Path.home()` for portability
- File locking detection and retry mechanism (5 retries, 2-second delays)
- Rotating file handler for logs (5MB max, 5 backup files)
- Year-based organization for time-series exports
- Support for monthly export naming patterns (`YYYY_MM_Monthly_CAD.xlsx`)
- Support for rolling 13-month export patterns (`YYYY_MM_to_YYYY_MM_Rolling13_*.xlsx`)
- Support for response time export patterns (`YYYY_MM_to_YYYY_MM_ResponseTime_*.xlsx`)
- Year extraction strategies: `start` and `end_range`
- Silent PowerShell launcher with duplicate detection
- Comprehensive documentation in `docs/` folder
- Directory Opus integration guides
- Git repository setup with `.gitignore`
- Project summary and README files

### Changed
- Replaced hardcoded paths with dynamic `Path.home()` references
- Improved logging with rotating file handler
- Enhanced file move operations with lock detection
- Reorganized directory structure (launchers, docs, logs, archive folders)
- Updated all launcher scripts to use new script name

### Deprecated
- `comprehensive_export_watchdog.py` (moved to `archive/`)
- Legacy log file format (now uses rotating logs)

### Fixed
- File locking issues when Excel files are open
- Duplicate event processing with debounce mechanism
- Path portability across different user accounts

## [1.0.0] - 2024-11-XX

### Added
- Initial release of comprehensive export watchdog
- Basic file monitoring for Desktop and Downloads folders
- Support for SCRPA CAD and RMS exports
- Support for OTActivity, TimeOffActivity, e_ticket exports
- Support for Backtracet_Arrests_Export
- Timestamp-prefixed file naming
- Basic logging functionality
- Windows Task Scheduler integration
- VBScript launcher for hidden execution

---

## Version History Summary

- **v2.0.0**: Major refactoring with modern architecture, year-based organization, and enhanced robustness
- **v1.0.0**: Initial release with basic file monitoring and organization

---

## Future Enhancements (Planned)

### [Unreleased]
- Configuration file support (YAML/JSON)
- Email notifications for failed moves
- Web dashboard for monitoring
- Support for additional export types
- Multi-user support
- Cloud storage integration options
- Performance metrics and reporting

