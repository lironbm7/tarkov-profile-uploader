@echo off
REM Start the SPT server and wait for it to close
start /wait "" "C:\SPT\SPT.Server.exe"

REM Run the upload script after the server shuts down
python "C:\SPT\scripts\upload_profiles.py"

REM Pause to see any messages before closing
pause