# SPT Profile Uploader

> ### 💡 Context
> When you play on a hosted server, your SPT (Single Player Tarkov) profile is only saved on that server. This means that when you switch to your own local server, you won’t have access to the profile's .json file since it was stored solely on the host machine. **The SPT Profile Uploader** addresses this issue by automatically uploading all profiles to a shared Google Drive, allowing players to easily download their profiles each time the server shuts down.


### Usage

To run the SPT server and upload profiles after the server shuts down, use the provided .bat file. This file will execute the server and subsequently invoke the upload script upon server shutdown.

### Configuration

1. Edit `constants.py` to use the correct paths for `PROFILES_DIRECTORY`, `CREDENTIALS_FILE_PATH`
2. Edit `run_spt_server.bat` to use the correct paths for `SPT_SERVER_DIRECTORY`, `SCRIPT_DIRECTORY`


### Google Drive Setup

1. Create a new SPT Profiles directory in your Google Drive where your profiles will be uploaded.

### Google API Setup

1. Create a new project in the Google Developers Console.
2. Enable the Google Drive API for your project.
3. Create and download the credentials.json file.

### Python Environment Setup

1. Create a virtual environment to manage your dependencies (`python -m venv venv`)

2. Activate the virtual environment (Windows: `venv\Scripts\activate`, macOS/Linux: `source venv/bin/activate`)

3. Install the required dependencies from the requirements.txt file (`pip install -r requirements.txt`)


### Screenshots

![image](https://github.com/user-attachments/assets/66875039-9a04-47f9-810b-ee5b231d2868)

![image](https://github.com/user-attachments/assets/0fba2cc9-416c-4d97-b2a7-fa66045f9a4b)
