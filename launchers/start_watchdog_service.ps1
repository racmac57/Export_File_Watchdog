# PowerShell script to start the Watchdog Service with duplicate check
# Can be used as a Directory Opus button command

Add-Type -AssemblyName System.Windows.Forms

$scriptDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog"
$scriptPath = Join-Path $scriptDir "watchdog_service.py"
$pythonExe = "pythonw.exe"

# Check if watchdog_service.py is already running
# Method: Check if any pythonw process has the script file open
$isRunning = $false
try {
    $processes = Get-Process pythonw -ErrorAction SilentlyContinue
    foreach ($proc in $processes) {
        try {
            $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $($proc.Id)").CommandLine
            if ($cmdLine -and $cmdLine -like "*watchdog_service.py*") {
                $isRunning = $true
                break
            }
        }
        catch {
            # If we can't check command line, try alternative method
            # Check if log file is being written to recently
            $logFile = Join-Path $scriptDir "logs\watchdog_service.log"
            if (Test-Path $logFile) {
                $logAge = (Get-Item $logFile).LastWriteTime
                if ((Get-Date) - $logAge -lt (New-TimeSpan -Minutes 2)) {
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

if ($isRunning) {
    [System.Windows.Forms.MessageBox]::Show(
        "Watchdog Service is already running!`n`nCheck the log file for activity:`n$scriptDir\logs\watchdog_service.log",
        "Watchdog Service",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )
    exit
}

# Change to script directory
Set-Location $scriptDir

# Start the service hidden
Start-Process -FilePath $pythonExe -ArgumentList "`"$scriptPath`"" -WindowStyle Hidden

# Wait a moment for process to start
Start-Sleep -Milliseconds 500

# Show confirmation
[System.Windows.Forms.MessageBox]::Show(
    "Watchdog Service started successfully!`n`nMonitoring:`n- Desktop`n- Downloads (OneDrive)`n- Downloads (Local)`n`nLog: $scriptDir\logs\watchdog_service.log",
    "Watchdog Service",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
)

