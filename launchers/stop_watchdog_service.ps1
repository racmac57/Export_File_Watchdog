# PowerShell script to stop the Watchdog Service
# Can be used as a Directory Opus button command

Add-Type -AssemblyName System.Windows.Forms

$scriptName = "watchdog_service.py"
$stopped = 0

# Find all pythonw processes
$pythonwProcesses = Get-Process pythonw -ErrorAction SilentlyContinue

if (-not $pythonwProcesses) {
    [System.Windows.Forms.MessageBox]::Show(
        "No pythonw processes found. Watchdog Service is not running.",
        "Watchdog Service",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )
    exit
}

# Check each pythonw process to see if it's running watchdog_service.py
foreach ($proc in $pythonwProcesses) {
    try {
        $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $($proc.Id)").CommandLine
        if ($cmdLine -and $cmdLine -like "*watchdog_service.py*") {
            Stop-Process -Id $proc.Id -Force -ErrorAction Stop
            $stopped++
        }
    }
    catch {
        # If we can't check command line, try to stop all pythonw processes
        # (less safe, but works if CIM query fails)
        try {
            Stop-Process -Id $proc.Id -Force -ErrorAction Stop
            $stopped++
        }
        catch {
            # Ignore errors for processes we can't stop
        }
    }
}

if ($stopped -gt 0) {
    [System.Windows.Forms.MessageBox]::Show(
        "Watchdog Service stopped successfully!`n`nStopped $stopped process(es).",
        "Watchdog Service",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )
}
else {
    [System.Windows.Forms.MessageBox]::Show(
        "No Watchdog Service processes found running.`n`n(No pythonw processes running watchdog_service.py)",
        "Watchdog Service",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )
}

