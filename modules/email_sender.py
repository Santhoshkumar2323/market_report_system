import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import settings
from modules.database import get_db_session
from modules.models import EmailLog
import time


def send_email(subject, html_content, report_id):
    recipients = settings.RECIPIENTS

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)

        for recipient in recipients:
            session = get_db_session()

            try:
                msg = MIMEMultipart("alternative")
                msg["From"] = settings.EMAIL_USER
                msg["To"] = recipient
                msg["Subject"] = subject

                msg.attach(MIMEText(html_content, "html"))

                server.sendmail(
                    settings.EMAIL_USER,
                    recipient,
                    msg.as_string()
                )

                log = EmailLog(
                    report_id=report_id,
                    recipient=recipient,
                    status="SENT",
                    error_message=None,
                )

                session.add(log)
                session.commit()

            except Exception as e:
                session.rollback()

                log = EmailLog(
                    report_id=report_id,
                    recipient=recipient,
                    status="FAILED",
                    error_message=str(e),
                )

                session.add(log)
                session.commit()

            finally:
                session.close()
            time.sleep(1)    