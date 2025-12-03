# PowerShell script to start the Watchdog Service silently (no popups, no taskbar)
# Can be used as a Directory Opus button command

# Suppress all errors and output
$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = "SilentlyContinue"

$scriptDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog"
$scriptPath = Join-Path $scriptDir "watchdog_service.py"
$pythonExe = "pythonw.exe"

# Check if watchdog_service.py is already running (silently, no popup)
$isRunning = $false
try {
    $processes = Get-Process pythonw -ErrorAction SilentlyContinue 2>$null
    foreach ($proc in $processes) {
        try {
            $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $($proc.Id)" -ErrorAction SilentlyContinue).CommandLine
            if ($cmdLine -and $cmdLine -like "*watchdog_service.py*") {
                $isRunning = $true
                break
            }
        }
        catch {
            # If we can't check command line, try alternative method
            # Check if log file is being written to recently
            $logFile = Join-Path $scriptDir "logs\watchdog_service.log"
            if (Test-Path $logFile -ErrorAction SilentlyContinue) {
                $logAge = (Get-Item $logFile -ErrorAction SilentlyContinue).LastWriteTime
                if ($logAge -and (Get-Date) - $logAge -lt (New-TimeSpan -Minutes 2)) {
                    $isRunning = $true
                    break
                }
            }
        }
    }
}
catch {
    # If process check fails, assume not running
    $isRunning = $false
}

# If already running, exit silently (no message)
if ($isRunning) {
    exit 0
}

# Change to script directory
try {
    Set-Location $scriptDir -ErrorAction SilentlyContinue
}
catch {
    # If directory change fails, continue anyway
}

# Start the service hidden (completely silent - no taskbar entry)
try {
    Start-Process -FilePath $pythonExe -ArgumentList "`"$scriptPath`"" -WindowStyle Hidden -ErrorAction SilentlyContinue | Out-Null
    exit 0
}
catch {
    # Exit silently even on error
    exit 0
}

