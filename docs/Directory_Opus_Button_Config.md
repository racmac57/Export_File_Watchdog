# Directory Opus Button Configuration Guide

Complete configuration details for each Watchdog Service launcher button.

---

## Button 1: Start Watchdog (VBScript - Silent)

**Description:** Starts the Watchdog Service silently using VBScript. No popups, no taskbar entry. Simple and lightweight. Does not check for duplicate instances.

**Type:** `Script Function`

**Script Type:** `VBScript`

**Command Editor Canvas (inline VBScript code):**
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog"
WshShell.Run "pythonw watchdog_service.py", 0, False
```

**Note:** For "Script Function" type, you must paste the VBScript code directly (not a file path). Directory Opus executes the code inline.

**Button Settings:**
- **Label:** `Start Watchdog`
- **Icon:** Play/Start icon (green arrow)
- **Wait for completion:** ❌ Unchecked
- **Show in:** Your choice (Toolbar, Context Menu, etc.)

---

## Button 2: Start Watchdog (PowerShell - Silent with Duplicate Check)

**Description:** Starts the Watchdog Service silently using PowerShell. Includes duplicate detection - if already running, exits silently without starting another instance. No popups, no taskbar entry. Recommended for automated use.

**Type:** `Standard Function (Opus or external)`

**Command Editor Canvas:**
```
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\start_watchdog_service_silent.ps1"
```

**Button Settings:**
- **Label:** `Start Watchdog (Silent)`
- **Icon:** Play/Start icon (green arrow)
- **Wait for completion:** ❌ Unchecked
- **Show in:** Your choice

---

## Button 3: Start Watchdog (PowerShell - With Confirmation)

**Description:** Starts the Watchdog Service using PowerShell with user feedback. Shows confirmation message when started successfully, and alerts if service is already running. Includes duplicate detection.

**Type:** `Standard Function (Opus or external)`

**Command Editor Canvas:**
```
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\start_watchdog_service.ps1"
```

**Button Settings:**
- **Label:** `Start Watchdog (Confirm)`
- **Icon:** Play/Start icon (green arrow)
- **Wait for completion:** ❌ Unchecked
- **Show in:** Your choice

---

## Button 4: Start Watchdog (Batch File)

**Description:** Starts the Watchdog Service using a batch file. Simple method, no duplicate checking. May briefly show a console window.

**Type:** `MS-DOS Batch Function`

**Command Editor Canvas:**
```
C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\start_watchdog_service.bat
```

**Button Settings:**
- **Label:** `Start Watchdog (Batch)`
- **Icon:** Play/Start icon
- **Wait for completion:** ❌ Unchecked
- **Show in:** Your choice

---

## Button 5: Stop Watchdog Service

**Description:** Stops the running Watchdog Service by finding and terminating all pythonw processes running watchdog_service.py. Shows confirmation message when stopped.

**Type:** `Standard Function (Opus or external)`

**Command Editor Canvas:**
```
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\stop_watchdog_service.ps1"
```

**Button Settings:**
- **Label:** `Stop Watchdog`
- **Icon:** Stop icon (red square/X)
- **Wait for completion:** ❌ Unchecked
- **Show in:** Your choice

---

## Quick Reference Table

| Button Name | Type | Command |
|------------|------|---------|
| **Start Watchdog (VBScript)** | Script Function | Inline VBScript (see Button 1 above) |
| **Start Watchdog (Silent)** | Standard Function | `powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\start_watchdog_service_silent.ps1"` |
| **Start Watchdog (Confirm)** | Standard Function | `powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\start_watchdog_service.ps1"` |
| **Start Watchdog (Batch)** | MS-DOS Batch Function | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\start_watchdog_service.bat` |
| **Stop Watchdog** | Standard Function | `powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\stop_watchdog_service.ps1"` |

---

## Recommended Setup

For most users, we recommend creating **two buttons**:

### 1. Start Button (Recommended: Silent PowerShell)
- **Type:** Standard Function (Opus or external)
- **Command:** 
  ```
  powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\start_watchdog_service_silent.ps1"
  ```
- **Why:** Silent operation, duplicate detection, no popups

### 2. Stop Button
- **Type:** Standard Function (Opus or external)
- **Command:**
  ```
  powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog\launchers\stop_watchdog_service.ps1"
  ```

---

## Step-by-Step: Adding a Button in Directory Opus

1. **Open Directory Opus**
2. **Right-click on toolbar** → **Customize** → **Toolbars**
3. **Select your toolbar** (e.g., "Main Toolbar")
4. **Click "New"** → **Button**
5. **In the Button Editor:**
   - **Label:** Enter button name (e.g., "Start Watchdog")
   - **Icon:** Click "..." to choose an icon
   - **Command tab:** Select the appropriate **Type** from dropdown
   - **Command Editor Canvas:** Paste the command from above
   - **Options tab:** Ensure "Wait for completion" is **unchecked**
6. **Click OK** to save

---

## Notes

- **Script Function** type requires inline VBScript code (paste the code directly, not a file path)
- **MS-DOS Batch Function** type is used for batch files (.bat) - paste the full path to the .bat file
- **Standard Function (Opus or external)** type is used for PowerShell scripts (.ps1) when calling via powershell.exe
- All launcher scripts use absolute paths, so they work regardless of current directory
- The service runs hidden (no console window, no taskbar entry)
- Logs are stored in: `Export_File_Watchdog\logs\watchdog_service.log`

**Important:** When using "Script Function" type, Directory Opus executes the code directly. Do NOT use `wscript.exe` command - paste the actual VBScript code instead.

---

## Troubleshooting

**Button doesn't work:**
- Verify the path is correct (copy-paste from this document)
- Check that Python is installed and in system PATH
- Try running the command manually in PowerShell/CMD to see errors
- Ensure "Wait for completion" is unchecked in button options

**Service doesn't start:**
- Check the log file: `Export_File_Watchdog\logs\watchdog_service.log`
- Verify Python is installed: `pythonw --version`
- Check if service is already running (use Stop button first)

**Multiple instances running:**
- Use the PowerShell launchers (they have duplicate detection)
- Or use the Stop button, then Start again

