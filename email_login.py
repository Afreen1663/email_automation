import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv 

EMAIL_SERVER = "smtp.gmail.com"
PORT = 587

#loading the environment
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")


def send_email(subject, receiver_email, name, due_date, invoice_no, amount):
  
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Travnook", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email


    msg.set_content(
        f"""\
        Hi {name},
        I hope you are doing well.
        I just wanted to drop you a quick note to remind you that {amount} AED in respect of our invoice {invoice_no} was due for payment {due_date}.
        I would be really grateful if you could confirm that everything is on track for payment. 
        Best Regards
        Afreen Hussain
        """
    )

    # HTML text
    msg.add_alternative(
        f"""\
    <html>
      <body>
        <p>Hi {name},</p>
        <p>I hope you are well.</p>
        <p>I just wanted to drop you a quick note to remind you that <strong>{amount} AED</strong> in respect of our invoice {invoice_no} was due for payment on <strong>{due_date}</strong>.</p>
        <p>I would be really grateful if you could confirm that everything is on track for payment.</p>
        <p>Best regards</p>
        <p>Afreen Hussain</p>
      </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="John Doe",
        receiver_email="afreenhussain1663@gmail.com",
        due_date="18, Aug 2026",
        invoice_no="INV-21-12-009",
        amount="5",
    )
