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
        # Compose email
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = f"New Contact Form Submission: {form.subject}"

        body = f"""
        Name: {form.name}
        Email: {form.email}
        Subject: {form.subject}
        Message:
        {form.message}
        """
        msg.attach(MIMEText(body, "plain"))

        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return {"message": "Contact form submitted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
