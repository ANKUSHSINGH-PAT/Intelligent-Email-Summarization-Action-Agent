import base64
import os
from datetime import datetime, timezone

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config.settings import (
    GMAIL_SCOPES,
    GOOGLE_CLIENT_SECRET_PATH,
    GOOGLE_TOKEN_PATH
)


def authenticate_gmail():
    creds = None

    if os.path.exists(GOOGLE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            GOOGLE_TOKEN_PATH, GMAIL_SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CLIENT_SECRET_PATH, GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(GOOGLE_TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return creds


def fetch_emails_today(max_results=10):
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    # Start of today (UTC)
    today_start = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    after_timestamp = int(today_start.timestamp())

    query = f"after:{after_timestamp}"

    results = service.users().messages().list(
        userId="me",
        q=query,
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        subject = get_header(msg_data, "Subject")
        body = extract_body(msg_data["payload"])

        emails.append({
            "subject": subject,
            "body": body
        })

    return emails


def get_header(message, name):
    for header in message["payload"]["headers"]:
        if header["name"] == name:
            return header["value"]
    return "No Subject"


def extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                return decode_body(part["body"]["data"])
    elif "body" in payload and "data" in payload["body"]:
        return decode_body(payload["body"]["data"])
    return ""


def decode_body(data):
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
