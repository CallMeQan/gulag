from os import getenv
import smtplib, ssl

def send_email(restore_link: str, server_email: str = "fuishere.ha.ha.ha@gmail.com",
               client_email: str = "phuhn.a1.2124@gmail.com") -> None:
    """
    Function to send email to an account to restore it.

    :restore_link: Link to restore the account.
    :sender_email: SERVER's email address that will send the restoring email.
    :sender_email: CLIENT's email address that will receive the restoring email.
    """
    # Replace with your own details
    password = getenv("PASSWORD_OF_EMAIL")  # Use the App Password here

    # Email content
    message = f"""\
Subject: Gulag account's restoration

This is the email from Gulag to restore your account.

Please click on this link: {restore_link}
"""

    # Gmail SMTP server configuration
    smtp_server = "smtp.gmail.com"
    port = 587  # 587 is used for TLS/STARTTLS

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Connect to the Gmail SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(server_email, password)  # Log in to your Gmail account
            server.sendmail(server_email, client_email, message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_email("this is your link")