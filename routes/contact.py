from fastapi import APIRouter, HTTPException
from models.contact import ContactForm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, RECEIVER_EMAIL

router = APIRouter()

@router.post("/contact")
def contact_us(form: ContactForm):
    try:
        # --- Email to RECEIVER (Admin) ---
        msg_to_receiver = MIMEMultipart()
        msg_to_receiver["From"] = SMTP_USER
        msg_to_receiver["To"] = RECEIVER_EMAIL
        msg_to_receiver["Subject"] = f"New Contact Form Submission: {form.subject}"

        body_receiver = f"""
        📬 New Contact Form Submission:

        Name: {form.name}
        Email: {form.email}
        Subject: {form.subject}
        Message:
        {form.message}
        """
        msg_to_receiver.attach(MIMEText(body_receiver, "plain"))

        # --- Thank You Email to USER (Sender) ---
        msg_to_user = MIMEMultipart()
        msg_to_user["From"] = SMTP_USER
        msg_to_user["To"] = form.email
        msg_to_user["Subject"] = "Thank you for contacting us!"

        body_user = f"""
        Hi {form.name},

        ✅ We’ve received your message and will get back to you soon!

        Your Message:
        -------------------------------
        Subject: {form.subject}
        Message: {form.message}

        Thanks again,
        The Support Team
        """
        msg_to_user.attach(MIMEText(body_user, "plain"))

        # --- Send Both Emails ---
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg_to_receiver)
            server.send_message(msg_to_user)

        return {"message": "Contact form submitted. Sender and receiver notified."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send emails: {str(e)}")
