import smtplib
from email.message import EmailMessage

def send_email(
    sender_email: str,
    password: str,
    to_email: str,
    subject: str,
    body: str
) -> str:
    try:
        # Prepare the email message
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Connect to the Gmail SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # Secure the connection
            smtp.login(sender_email, password)
            smtp.send_message(msg)

        return f"✅ Email sent successfully to: {to_email}"

    except smtplib.SMTPAuthenticationError:
        return "❌ Authentication failed. Please check your email and app password."

    except smtplib.SMTPRecipientsRefused:
        return f"❌ The recipient's email address was refused: {to_email}"

    except smtplib.SMTPConnectError:
        return "❌ Could not connect to the SMTP server. Please check your internet connection."

    except smtplib.SMTPException as e:
        return f"❌ SMTP error: {str(e)}"

    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"
