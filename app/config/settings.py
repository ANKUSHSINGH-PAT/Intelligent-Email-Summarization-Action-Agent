import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

GOOGLE_CLIENT_SECRET_PATH = os.getenv(
    "GOOGLE_CLIENT_SECRET_PATH",
    "credentials/client_secret.json"
)

GOOGLE_TOKEN_PATH = os.getenv(
    "GOOGLE_TOKEN_PATH",
    "credentials/token.json"
)

MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 300))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))
