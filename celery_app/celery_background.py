import time
from fastapi import FastAPI
from celery import shared_task, Celery

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
	CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL","redis://127.0.0.1:6379/0")
	CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND","redis://127.0.0.1:6379/0")


settings = Config()

app = FastAPI()

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)


@celery.task
def send_push_notification(device_token: str):
    time.sleep(10)  # simulates slow network call to firebase/sns
    with open("notification.log", mode="a") as notification_log:
        response = f"Successfully sent push notification to: {device_token}\n"
        notification_log.write(response)


@app.get("/push/{device_token}")
async def notify(device_token: str):
    send_push_notification.delay(device_token)
    return {"message": "Notification sent"}

