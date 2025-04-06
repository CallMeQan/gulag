import smtplib, ssl
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Replace with your own details
sender_email = "hongp4949@gmail.com"
receiver_email = "cptrekkles@gmail.com"
password = os.getenv("EMAIL_PASSWORD")  # Use the App Password here

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
try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be used to identify the client to the server
        server.starttls(context=context)  # Secure the connection using TLS
        server.ehlo()  # Re-identify after starting TLS
        server.login(sender_email, password)  # Log in to your Gmail account
        server.sendmail(sender_email, receiver_email, message)  # Send the email
        print("Email sent successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
