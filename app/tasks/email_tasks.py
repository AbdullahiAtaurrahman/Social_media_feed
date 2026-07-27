from app.tasks.celery_app import celery_app
import time


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email_task(self, email: str, username: str):
    """
    Celery task: send welcome email.
    bind=True gives access to self (the task instance).
    max_retries=3 retries up to 3 times before marking failed.
    default_retry_delay=60 waits 60s between retries.
    """
    try:
        # Replace with real email library (e.g. sendgrid, smtp)
        print(f"[EMAIL] Welcome to PostIt, {username}! -> {email}")
        time.sleep(2)  # simulate network IO
        return {"status": "sent", "email": email}
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task
def send_password_reset_task(email: str, reset_token: str):
    print(f"[EMAIL] Password reset for {email}, token={reset_token}")
    return {"status": "sent"}
