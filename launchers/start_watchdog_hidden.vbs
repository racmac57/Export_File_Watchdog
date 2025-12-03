Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Export_File_Watchdog"
WshShell.Run "pythonw watchdog_service.py", 0, False