import smtplib, ssl
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Get the email password from environment variable

# Replace with your own details
sender_email = "hongp4949@gmail.com"
receiver_email = "phuhn.a1.2124@gmail.com"
password = os.getenv("EMAIL_PASSWORD")  # Use an app password if 2FA is enabled

# Email content
message = """\
Subject: Test Email from Python

This is a test email sent using Gmail's SMTP server.
"""

# Gmail SMTP server configuration
smtp_server = "smtp.gmail.com"
port = 587  # 587 is used for TLS/STARTTLS

# Create a secure SSL context
context = ssl.create_default_context()

# Connect to the Gmail SMTP server and send the email
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be used to identify the client to the server
    server.starttls(context=context)  # Secure the connection using TLS
    server.ehlo()  # Re-identify after starting TLS
    server.login(sender_email, password)  # Log in to your Gmail account
    server.sendmail(sender_email, receiver_email, message)  # Send the email
    print("Email sent successfully!")
# Note: Make sure to enable "Less secure app access" in your Google account settings if you're not using 2FA.