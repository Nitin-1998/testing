from app.email_fetcher import extract_otp_from_email

otp = extract_otp_from_email()
print("Received OTP:", otp)