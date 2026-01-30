from services.gmail_service import fetch_emails_today
from services.summarizer import summarize_emails

def main():
    emails = fetch_emails_today()

    if not emails:
        print("📭 No emails for today")
        return

    summaries = summarize_emails(emails)

    for i, (email, summary) in enumerate(zip(emails, summaries), 1):
        print("\n" + "=" * 60)
        print(f"📧 Email {i}")
        print("Subject:", email["subject"])
        print("\n🧠 Summary:")
        print(summary)

if __name__ == "__main__":
    main()
