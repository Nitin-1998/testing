import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import re

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 993))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FILTER_SENDER = os.getenv("EMAIL_FILTER_SENDER")


def extract_otp_from_email():
    mail = imaplib.IMAP4_SSL(EMAIL_HOST, EMAIL_PORT)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    search_criteria = f'(FROM "{EMAIL_FILTER_SENDER}")'
    status, messages = mail.search(None, search_criteria)

    if status != "OK" or not messages[0]:
        print("❌ No matching unread emails.")
        return

    email_ids = messages[0].split()
    latest_email_id = email_ids[-1:]  # only the last one
    print(f"📬 Found {len(email_ids)} unread emails from {EMAIL_FILTER_SENDER}")

    for email_id in latest_email_id:
        res, msg_data = mail.fetch(email_id, "(RFC822)")
        if res != 'OK':
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg["Subject"])[0]
        subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject

        print(f"🔍 Reading: {subject}")

        body = ""
        for part in msg.walk():
            content_type = part.get_content_type()

            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                try:
                    body = payload.decode("utf-8")
                except UnicodeDecodeError:
                    body = payload.decode("latin1")
                break

            elif content_type == "text/html":
                payload = part.get_payload(decode=True)
                try:
                    html_body = payload.decode("utf-8")
                except UnicodeDecodeError:
                    html_body = payload.decode("latin1")
                body = re.sub("<[^<]+?>", "", html_body)
                break
        else:
            body = ""

        # Find OTP
        match = re.search(r"One Time Sign[- ]In code[:：]?\s*(\d+)", body)
        if match:
            otp = match.group(1)
            print(f"✅ Extracted OTP: {otp}")
            return otp
        else:
            print("❌ No OTP found in email body.")

    mail.logout()
