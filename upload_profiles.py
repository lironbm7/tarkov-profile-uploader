import os
import glob
import pickle
from typing import Optional

from googleapiclient.discovery import build, Resource
from google.auth.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from constants import (
    CREDENTIALS_FILE_PATH,
    PROFILES_DIRECTORY,
    PROFILES_DIRECTORY_IN_GOOGLE_DRIVE,
    SCOPES,
    TOKEN_PICKLE,
)


def load_credentials() -> Optional[Credentials]:
    """Load saved credentials from the token file if available.

    Returns:
        Optional[Credentials]: The loaded credentials object if available, otherwise None.
    """
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            return pickle.load(token)
    return None


def authenticate_with_google() -> Optional[Credentials]:
    """Authenticate the user with Google and return the credentials object.

    This function loads existing credentials if they are valid. If not, it prompts the user to log in
    and saves the newly obtained credentials for future use.

    Returns:
        Optional[Credentials]: The authenticated credentials object, or None if authentication fails.
    """
    creds = load_credentials()

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def find_or_create_folder(service: Resource, folder_name: str) -> str:
    """Find or create a folder in Google Drive.

    This function checks for the existence of a folder with the specified name. 
    If it exists, the function returns its ID; otherwise, it creates a new folder
    with the given name and returns the new folder's ID.

    Args:
        service (Resource): The Google Drive API service.
        folder_name (str): The name of the folder to find or create.

    Returns:
        str: The ID of the found or created folder in Google Drive.
    """
    response = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
        spaces='drive',
        fields='files(id, name)'
    ).execute()
    folders = response.get('files', [])
    if folders:
        return folders[0]['id']
    else:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')


def upload_files_from_directory(directory: str) -> None:
    """Upload all files from a specified directory to the "/spt-profiles/" folder in Google Drive.

    This function authenticates with Google Drive, finds or creates the specified folder,
    and uploads all files in the specified local directory to that folder.

    Args:
        directory (str): The local directory containing the files to upload.

    Raises:
        Exception: If authentication with Google fails.
    """
    creds = authenticate_with_google()
    if not creds:
        raise Exception("Google authentication failed. Unable to upload files.")

    service = build('drive', 'v3', credentials=creds)
    folder_id = find_or_create_folder(service, PROFILES_DIRECTORY_IN_GOOGLE_DRIVE)

    for filepath in glob.glob(os.path.join(directory, '*')):
        if os.path.isfile(filepath):
            try:
                file_metadata = {
                    'name': os.path.basename(filepath),
                    'parents': [folder_id]
                }
                media = MediaFileUpload(filepath)
                service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(f'Uploaded: {filepath}')
            except HttpError as error:
                print(f"Failed to upload {filepath}: {error}")


if __name__ == '__main__':
    upload_files_from_directory(PROFILES_DIRECTORY)
