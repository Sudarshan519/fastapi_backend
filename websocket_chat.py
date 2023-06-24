import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <style>ul { list-style-type: none; }
    body{
    margin-bottom:80px;
    }
    div{
    height:50px;
    width:50px;
    background:red;
    }
    #messageText{
    
    width:60vw;
    padding:6px;
    border-radius:14px;
    height:7vh;
    }
    button{
    height:7vh;
    width:32vw;border-radius:14px;
    }

    li{
    padding:8px;
           border-radius:.5rem;  border: solid 1px #3772ff;
            margin-bottom:10px;
    }
    li.left{ 
   
    margin-left:300px;
        display: block;
  text-align: right;
   align-items: flex-end;
  
     
    border:solid 1px #3772ff
     position: relative; 
    }
    li.right{  
    margin-right:300px;
     display: block;
  text-align: left;
      position: relative; 
     border:solid 1px #3772ff
   text-align:right;
     align-items: flex-start;
    }

    form{
    position:fixed;
    bottom:10px;
    right:0;
    }
    </style>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" placeholder="Enter your message"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var loc=window.location.href;
        console.log(loc)
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://${window.location.host}/ws/${client_id}`);
            console.log(ws);
            
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                 var content = document.createTextNode(event.data)
                 let data=JSON.parse(event.data)
                
                console.log(event)
                let markup=`<h4>${data.id}</h4>
               <p>${event.data}</p>`
               console.log(markup)
               message.innerHTML=markup
                if(event.data.includes(client_id))
                
               { message.classList.add("left");
               }
                else
                { message.classList.add("right")}
               
                message.appendChild(content)
              
                messages.appendChild(message)
                window.scrollTo(0, document.body.scrollHeight);
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
#   message.appendChild(document.createElement("div").appendChild(document.createTextNode("HELLO")))

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        await websocket.send_text("Hello from server")
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(json.dumps({'id':'server','data':f"Client #{client_id} says: {data}"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({"id":"server","data":f"Client #{client_id} left the chat"}))