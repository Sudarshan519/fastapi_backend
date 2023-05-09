import time
from fastapi import FastAPI,BackgroundTasks

app = FastAPI()


def send_push_notification(device_token: str):
    time.sleep(15)  # simulates slow network call to firebase/sns
    with open("notification.log", mode="a") as notification_log:
        response = f"Successfully sent push notification to {device_token}\n"
        notification_log.write(response)


@app.get("/push/{device_token}")
async def notify(device_token: str,background_tasks:BackgroundTasks):
    background_tasks.add_task(send_push_notification,device_token)
    return {"message": "Notification sent"}
