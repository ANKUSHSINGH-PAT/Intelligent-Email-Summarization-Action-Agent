import os
from groq import Groq

from config.prompts import EMAIL_SUMMARY_PROMPT
from config.settings import MODEL_NAME, MAX_TOKENS, TEMPERATURE
from utils.email_parser import clean_email_text

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_emails(emails):
    summaries = []

    for email in emails:
        body = clean_email_text(email["body"])
        email_text = f"Subject: {email['subject']}\n\n{body}"

        prompt = EMAIL_SUMMARY_PROMPT.format(
            email_text=email_text
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,   # e.g. "llama3-8b-8192"
            messages=[
                {
                    "role": "system",
                    "content": "You summarize emails clearly and concisely."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        summary = response.choices[0].message.content.strip()
        summaries.append(summary)

    return summaries
