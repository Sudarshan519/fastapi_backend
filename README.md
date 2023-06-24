# fastapi_backend

# serve local server
uvicorn websocket_chat:app --host 0.0.0.0 --port 8080 

# run chat app
uvicorn websocket_chat:app --bind 0.0.0.0:80