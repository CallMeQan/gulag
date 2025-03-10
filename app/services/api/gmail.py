import os.path
import base64
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_latest_email() -> str | None:
    """
    Fetches the latest email from the user's inbox and saves it as a JSON file with body type detection.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId="me", maxResults=1).execute()
        messages = results.get("messages", [])

        if not messages:
            print("No messages found.")
            return
        msg = service.users().messages().get(userId="me", id=messages[0]["id"], format="full").execute()
        
        email_data = {
            "from": "",
            "subject": "",
            "body": None,
            "body_type": None
        }

        for header in msg["payload"]["headers"]:
            if header["name"] == "Subject":
                email_data["subject"] = header["value"]
            if header["name"] == "From":
                email_data["from"] = header["value"]

        def decode_body(part):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")

        if "parts" in msg["payload"]:
            for part in msg["payload"]["parts"]:
                if part["mimeType"] == "text/html":
                    email_data["body"] = decode_body(part)
                    email_data["body_type"] = "text/html"
                    break  # Prefer HTML if available
                elif part["mimeType"] == "text/plain" and email_data["body"] is None:
                    email_data["body"] = decode_body(part)
                    email_data["body_type"] = "text/plain"

        soup = BeautifulSoup(email_data["body"], "html.parser")

        for a in soup.find_all("a", href=True):
            if "amazonaws" in a["href"]:
                return a["href"]
        return None
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

if __name__ == "__main__":
    print(get_latest_email())
