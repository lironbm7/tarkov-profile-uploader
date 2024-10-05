@echo off

REM Directory Definitions
set "SPT_SERVER_DIRECTORY=C:\SPT"
set "SCRIPT_DIRECTORY=C:\SPT\tarkov-profile-uploader"

REM File paths based on directory definitions
set "SPT_SERVER_PATH=%SPT_SERVER_DIRECTORY%\SPT.Server.exe"
set "UPLOAD_SCRIPT_PATH=%SCRIPT_DIRECTORY%\upload_profiles.py"
set "PYTHON_EXEC_PATH=%SCRIPT_DIRECTORY%\venv\Scripts\python.exe"

REM Change to the SPT Server directory
cd "%SPT_SERVER_DIRECTORY%"
echo Starting SPT Server at "%SPT_SERVER_PATH%"...

REM Start the SPT server and wait for it to close
start /wait "" "%SPT_SERVER_PATH%"

REM Run the upload script using the Python executable from the virtual environment
echo SPT Server has shut down. Starting upload process...
cd "%SCRIPT_DIRECTORY%"
"%PYTHON_EXEC_PATH%" "%UPLOAD_SCRIPT_PATH%"
echo Upload process completed.

REM Pause to see any messages before closing
pause
