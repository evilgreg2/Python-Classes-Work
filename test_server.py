from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from uvicorn import run
from secrets import token_hex

app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name= "static")


users = {}
tokens = {}
favorites = {}
chats = {}

users["fake1"] = "password1"
users["fake2"] = "password2"

@app.get("/user/signup")
def signup(username: str, password: str):
    if username in users:
        raise HTTPException(status_code = 400)
    users[username] = password
    favorites[username] = []
    return "OK"

@app.get("/user/signin")
def signin(username: str, password: str) -> str:
    if username not in users:
        raise HTTPException(staus_code = 400)
    saved_password = users[username]
    if password != saved_password:
        raise HTTPException(status_code = 400)
    token = token_hex(16)
    tokens[token] = username
    return token

@app.get("/user/search")
def search(token: str, prefix: str):
    if token not in tokens:
        raise HTTPException(status_code = 400)
    
    if len(prefix) < 3:
        return []
    
    result = []
    for username in users.keys():
        if prefix in username:
            result.append(username)
    return result



@app.get("/favorite/add")
def add_to_favorites(token: str, favorite_name: str): 
    if token not in tokens:
        raise HTTPException(status_Code = 400)
    username = tokens[token]
    favorites[username].append(favorite_name)
    pair = frozenset((username, favorite_name))
    chats[pair] = []
    print(favorite_name , favorites , chats)


@app.get("/favorite/list")
def get_list_of_favorites(token: str):
    if token not in tokens:
        raise HTTPException(status_code = 400)
    username = tokens[token]
    friends = favorites[username]

    result = []
    for f in friends:
        result.append({
            "imgLink": "https://i.pravatar.cc/100?id=2",
            "time": "5:11PM",
            "username": f,
            "lastMsg": "message here",
            "counter": "1",
        })

    return result


@app.get("/chat")
def get_messages(token: str, favorite_name: str):
    if token not in tokens:
        raise HTTPEsception(status_code = 400)
    username = tokens[token]
    pair = frozenset((username, favorite_name))
    return {
        "username": "Elizabeth",
        "lastVisit": "1727227624",
        "messages": [
            {
                "text": "I am some message",
                "time": "1727227524",
                "author": "Elizabeth",
            },
            {
                "text": "I am another message",
                "time": "17227237510",
                "author": "Greg",
            }
        ]
    }

@app.get("/chat/send")
def send_message(token: str, favorite_name: str, message_body: str):
    if token not in tokens:
        raise HTTPException(status_code = 400)
    username = tokens[token]
    pair = frozenset((username, favorite_name))
    chats[pair].append(message_body)


run(app)