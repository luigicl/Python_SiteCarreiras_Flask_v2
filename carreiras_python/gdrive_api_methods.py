from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from oauth2client.service_account import ServiceAccountCredentials
import io
import os

PARENT_FOLDER_ID = "1YptqBEPPfzBj2ynWPupPgouKcCXLGWkC"


class GoogleDriveService:
    def __init__(self):
        self._SCOPES = ['https://www.googleapis.com/auth/drive']
        _base_path = os.path.dirname(__file__)
        # _credential_path = os.path.join(_base_path, r'carreiras_python\service_account.json')
        _credential_path = 'carreiras_python/service_account.json'
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _credential_path

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"), self._SCOPES)
        service = build('drive', 'v3', credentials=creds)
        return service

    def upload_file(self, file, file_name):
        # creds = __authenticate()
        # service = __build_service(creds)
        service = GoogleDriveService().build()
        uploaded_file = file
        buffer = io.BytesIO()  # creating a buffer memory
        buffer.name = uploaded_file.filename
        uploaded_file.save(buffer)  # saving file to buffer memory
        media = MediaIoBaseUpload(buffer, mimetype=uploaded_file.mimetype, resumable=True)
        returned_fields = "id, name, mimeType, webViewLink, exportLinks"
        request = service.files().create(
            media_body=media,
            body={'name': file_name, 'parents': [PARENT_FOLDER_ID]},
            fields=returned_fields
        ).execute()
        file_id = request.get("id")
        return file_id

    def delete_file(self, file_id):
        service = GoogleDriveService().build()
        service.files().delete(fileId=file_id).execute()
