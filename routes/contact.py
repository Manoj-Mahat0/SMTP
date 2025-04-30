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
        # --- 1. Compose notification email to RECEIVER_EMAIL ---
        msg_to_receiver = MIMEMultipart()
        msg_to_receiver["From"] = SMTP_USER
        msg_to_receiver["To"] = RECEIVER_EMAIL
        msg_to_receiver["Subject"] = f"New Contact Form Submission: {form.subject}"

        body = f"""
        Name: {form.name}
        Email: {form.email}
        Subject: {form.subject}
        Message:
        {form.message}
        """
        msg_to_receiver.attach(MIMEText(body, "plain"))

        # --- 2. Compose thank-you email to the user ---
        msg_to_user = MIMEMultipart()
        msg_to_user["From"] = SMTP_USER
        msg_to_user["To"] = form.email
        msg_to_user["Subject"] = "Thank you for contacting us!"

        thank_you_body = f"""
        Dear {form.name},

        Thank you for reaching out! We have received your message and will get back to you as soon as possible.

        Here’s a copy of your message:
        -----------------------------------
        Subject: {form.subject}
        Message: {form.message}

        Best regards,
        Support Team
        """
        msg_to_user.attach(MIMEText(thank_you_body, "plain"))

        # --- 3. Send both emails ---
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg_to_receiver)
            server.send_message(msg_to_user)

        return {"message": "Contact form submitted successfully and confirmation email sent"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
