Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Watchdog"
WshShell.Run "pythonw comprehensive_export_watchdog.py", 0, False