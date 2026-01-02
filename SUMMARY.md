# Export File Watchdog Service - Project Summary

## Overview

The **Export File Watchdog Service** is an automated file monitoring and organization system designed to streamline ETL (Extract, Transform, Load) workflows for the City of Hackensack. It automatically detects export files in designated folders and organizes them into a structured directory hierarchy with year-based subfolders for time-series data.

## Problem Statement

Manual file organization is time-consuming and error-prone, especially when dealing with:
- Multiple export types (CAD, RMS, overtime, summons, etc.)
- Time-series data requiring year-based organization
- Files downloaded to various locations (Desktop, Downloads)
- Files that may be locked when open in Excel
- Need for consistent naming conventions and directory structure

## Solution

An automated background service that:
1. **Monitors** Desktop and Downloads folders continuously
2. **Detects** export files based on naming patterns
3. **Extracts** year information from time-series filenames
4. **Organizes** files into structured directories with year subfolders
5. **Handles** locked files gracefully with retry logic
6. **Logs** all operations for audit and troubleshooting

## Key Features

### Core Functionality
- ✅ Real-time file system monitoring
- ✅ Pattern-based file detection
- ✅ Automatic directory creation
- ✅ Year extraction from filenames
- ✅ File locking detection and retry
- ✅ Silent background operation

### Export Types Supported
- **Legacy**: SCRPA CAD/RMS, Overtime, Time Off, E-Tickets, Backtrace Arrests, LawSoft Arrests
- **Time-Series**: Monthly exports, Rolling 13-month, Response Time reports
- **Benchmark Reports**: Vehicle Pursuit, Use of Force, Show of Force (with overwrite behavior)
- **Excel Conversion**: Automatic conversion of specific `.xlsx` files to `.csv` format on desktop

### Technical Features
- Object-oriented Python architecture
- Dynamic path resolution (portable across users)
- Rotating log files (prevents disk space issues)
- Duplicate instance prevention
- Multiple launcher options (VBScript, PowerShell, Batch)

## Architecture

### Components

1. **FileMover Class**
   - Handles file operations
   - Detects locked files
   - Implements retry logic

2. **YearExtractor Class**
   - Extracts year from filenames
   - Supports multiple extraction strategies
   - Handles edge cases

3. **ExportWatchdogHandler Class**
   - Main event handler
   - Manages file system events
   - Coordinates file processing

4. **Launcher Scripts**
   - Multiple options for different use cases
   - Silent and interactive modes
   - Duplicate detection

## Use Cases

1. **Automated File Organization**
   - User downloads export → Automatically organized by type and year

2. **ETL Pipeline Integration**
   - Export files automatically sorted for downstream processing

3. **Compliance & Audit**
   - Consistent file organization
   - Complete operation logs

4. **Multi-User Environment**
   - Portable paths work across different user accounts

## Technology Stack

- **Language**: Python 3.8+
- **Libraries**: watchdog (file system monitoring)
- **Platform**: Windows (designed for Windows file system)
- **Integration**: Directory Opus, Windows Task Scheduler

## Project Status

✅ **Production Ready** - Version 2.1.0

- Fully functional and tested
- Comprehensive documentation
- Ready for GitHub deployment
- Suitable for production use
- Supports 25+ export types with automatic organization
- Organized directory structure with year-based subfolders
- Multiple year extraction strategies for different file naming patterns

## Future Roadmap

- Configuration file support
- Email notifications
- Web dashboard
- Additional export types
- Performance metrics

## Repository Information

- **Name**: Export File Watchdog Service
- **Directory**: Export_File_Watchdog (renamed from Watchdog)
- **Version**: 2.1.0
- **License**: MIT
- **Maintainer**: City of Hackensack IT Department

## Recent Changes (v2.1.0)

### Major Additions
- **Yearly Exports**: Support for yearly CAD, RMS, and Arrest exports
- **Arrest Exports**: Monthly and yearly arrest exports with Lawsoft variant support
- **NIBRS Reports**: PDF report monitoring for monthly and yearly NIBRS Agency Summary Reports
- **Benchmark Reports Restructured**: Complete reorganization into complete_report, officer_report, and summary categories
- **Enhanced Year Extraction**: New strategies for extracting years from various date range patterns

### Improvements
- Better directory organization with category-based subdirectories
- Support for files saved directly to export folders
- Improved file routing based on naming patterns

### Removed
- Excel to CSV conversion (removed due to duplicate file creation issues)

---

*Last Updated: January 2026*

