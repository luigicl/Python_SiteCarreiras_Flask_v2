from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import io


SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = "1YptqBEPPfzBj2ynWPupPgouKcCXLGWkC"


def __authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds


def __build_service(creds):
    build_service = build('drive', 'v3', credentials=creds)
    return build_service


def upload_file(file, file_name):
    creds = __authenticate()
    service = __build_service(creds)
    uploaded_file = file
    buffer = io.BytesIO()
    buffer.name = uploaded_file.filename
    uploaded_file.save(buffer)
    media = MediaIoBaseUpload(buffer, mimetype=uploaded_file.mimetype, resumable=True)
    request = service.files().create(
        media_body=media,
        body={'name': file_name, 'parents': [PARENT_FOLDER_ID]},
        fields='id'
    ).execute()
    file_id = request.get("id")
    return file_id


def delete_file(file_id):
    creds = __authenticate()
    service = __build_service(creds)
    service.files().delete(fileId=file_id).execute()
