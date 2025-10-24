#AgentCodeStarted
import os
import logging
from flask import request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Optional
import json

LOG_DIR = "/data/logs/3c48e1ed2f594049/"
LOG_FILE = os.path.join(LOG_DIR, "workflow.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, filemode="a", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# list of emails
recipient_email = [

] 

def send_compliance_email(
    sender_email: str,
    sender_password: str,
    recipient_email: List[str],  
    #compliance_status: str,
    report: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
    use_html: bool = False,
    attachments: Optional[List[str]] = None,
) -> bool:
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipient_email)  
        msg["Subject"] = "Compliance Status Report"

        if use_html:
            body = f"""
            <html>
            <body>
                <h2>Compliance Status Enclosed</h2>
                <p><strong>Report:</strong></p>
                 <pre>this is only a test. i repeat this is only a test</pre>
                <pre>{report}</pre>
            </body>
            </html>
            """
            msg.attach(MIMEText(body, "html"))
        else:
            body = f"Compliance Status Enclosed\n\nReport:\n{report}"
            msg.attach(MIMEText(body, "plain"))

        if attachments:
            for filepath in attachments:
                if os.path.isfile(filepath):
                    with open(filepath, "rb") as file:
                        part = MIMEApplication(
                            file.read(), Name=os.path.basename(filepath)
                        )
                        part["Content-Disposition"] = (
                            f'attachment; filename="{os.path.basename(filepath)}"'
                        )
                        msg.attach(part)
                else:
                    print(f"Attachment not found: {filepath}")

        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email, recipient_email, msg.as_string()
            )  

        print("Email sent successfully.")
        return True

    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return False
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return False

def main():
    try:
        logging.info("***************Email Sender Agent triggered***************")
      
        data = request.get_json(force=True)
        logging.info("request data: %s", data)
        #compliance_status = data.get("compliance_status") cognitive agent only sends one message, not multiple

        report = data.get("compliance_status")

        '''
        add environment secrets
        '''
        gmail_username = data.get("gmail_username")
        gmail_password = data.get("gmail_password")

        result = send_compliance_email(
            sender_email=gmail_username,
            sender_password=gmail_password,
            recipient_email=recipient_email,
            #compliance_status=compliance_status,
            report=report
        )

        if result:
            logging.info("Email sent successfully")
            output = {
                "status": "success",
                "message": "Email sent successfully"
            }
        else:
            logging.error("Failed to send email")
            output = {
                "status": "error",
                "message": "Failed to send email"
            }
        return output
    except Exception as e:
        logging.error("Exception: %s", str(e))
        return {
            "status": "error",
            "message": str(e)
        }

#AgentCodeEnded