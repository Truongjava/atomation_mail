from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import smtplib
from email.message import EmailMessage
import json

app = FastAPI(title="Multi-SMTP Mail Sender API")

# Load SMTP cấu hình từ file JSON
with open("smtp_config.json", "r") as f:
    SMTP_CONFIGS = json.load(f)

def send_email(subject, body, to_email, smtp_conf):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_conf["user"]
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(smtp_conf["server"], smtp_conf["port"]) as server:
        server.starttls()
        server.login(smtp_conf["user"], smtp_conf["pass"])
        server.send_message(msg)

@app.post("/send-email")
async def send_email_api(
    to_email: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    provider: str = Form(...)
):
    if provider not in SMTP_CONFIGS:
        return JSONResponse(content={"error": "Invalid provider"}, status_code=400)
    
    try:
        send_email(subject, body, to_email, SMTP_CONFIGS[provider])
        return {"message": f"Email sent successfully from {SMTP_CONFIGS[provider]['user']}"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
