# Directory Opus Watchdog Service Button Setup

This guide explains how to add buttons to Directory Opus to start and stop the Watchdog Service.

## Available Launcher Scripts

All launcher scripts are located in the `launchers/` subdirectory:

1. **launchers/start_watchdog_service.vbs** - Simple VBScript launcher (no duplicate check, completely silent)
2. **launchers/start_watchdog_service.bat** - Batch file launcher (simple, no duplicate check)
3. **launchers/start_watchdog_service.ps1** - PowerShell launcher (checks for duplicates, shows confirmation)
4. **launchers/start_watchdog_service_silent.ps1** - PowerShell launcher (checks for duplicates, no popups, completely silent)
5. **launchers/stop_watchdog_service.ps1** - PowerShell script to stop the service

## Recommended: PowerShell Script (with duplicate check)

### Step 1: Create Start Button

1. In Directory Opus, go to **Tools** → **Customize** → **Toolbars**
2. Select the toolbar where you want the button (e.g., "Main Toolbar")
3. Click **New** → **Button**
4. Configure the button:
   - **Label**: `Start Watchdog`
   - **Icon**: Choose an appropriate icon (e.g., play/start icon)
   - **Command**: 
     ```
     powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog\launchers\start_watchdog_service.ps1"
     ```
   - **Working Directory**: Leave empty or set to Watchdog directory
   - **Show in**: Choose where you want it visible

### Step 2: Create Stop Button

1. Follow the same steps as above
2. Configure:
   - **Label**: `Stop Watchdog`
   - **Icon**: Choose a stop icon
   - **Command**:
     ```
     powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog\launchers\stop_watchdog_service.ps1"
     ```

### Alternative: Simple VBScript Method

If you prefer a simpler approach without duplicate checking:

**Command for Start Button:**
```
wscript.exe "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog\launchers\start_watchdog_service.vbs"
```

**Or for silent version (no popups):**
```
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog\launchers\start_watchdog_service_silent.ps1"
```

**Command for Stop Button:**
```
powershell.exe -Command "Get-Process pythonw | Where-Object {$_.CommandLine -like '*watchdog_service.py*'} | Stop-Process -Force"
```

## Quick Setup (Copy-Paste Commands)

### Start Button Command (with confirmation):
```
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog\launchers\start_watchdog_service.ps1"
```

### Start Button Command (silent, no popups):
```
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog\launchers\start_watchdog_service_silent.ps1"
```

### Stop Button Command:
```
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog\launchers\stop_watchdog_service.ps1"
```

## Testing

1. Click the **Start Watchdog** button
2. You should see a confirmation message (if using PowerShell script)
3. Check the log file: `Watchdog\logs\watchdog_service.log`
4. Try downloading/creating a test export file to verify it's working

## Notes

- The PowerShell scripts require execution policy to be set (use `-ExecutionPolicy Bypass` flag)
- The VBScript and batch file methods don't check for duplicates - multiple instances could run
- The PowerShell method shows a message box if the service is already running
- All methods run the service hidden (no console window)

## Troubleshooting

**If the button doesn't work:**
1. Verify the path to the script is correct
2. Check that Python is in your system PATH
3. Try running the script manually from PowerShell to see any errors
4. Check Directory Opus button settings - ensure "Wait for completion" is unchecked

**To check if service is running:**
```powershell
Get-Process pythonw | Where-Object {$_.CommandLine -like '*watchdog_service.py*'}
```

**To manually stop all instances:**
```powershell
Get-Process pythonw | Where-Object {$_.CommandLine -like '*watchdog_service.py*'} | Stop-Process -Force
```

