# A Bare Bones Slack API
# Illustrates basic usage of FastAPI
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
import requests
import json
from fastapi.middleware.cors import CORSMiddleware

# Message class defined in Pydantic
class Message(BaseModel):
    channel: str
    author: str
    text: str

# Instantiate the FastAPI
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# In a real app, we would have a database.
# But, let's keep it super simple for now!
channel_list = ["general", "dev", "marketing"]
message_map = {}
for channel in channel_list:
    message_map[channel] = []

@app.get("/authen/{user}/{password}")
def get_status(user:str,password:str):
    response_authen = requests.get("http://indyinter.duckdns.org:8081/authen/"+user+"/"+password)
    data = response_authen.text
    json_authen = json.loads(data)
    return json_authen


@app.get("/{code}") 
def read_code(code: str):
  response_code = requests.get("http://indyinter.duckdns.org:8081/"+code)
  data = response_code.text
  json_code = json.loads(data)
  return json_code


@app.get("/channels", response_model=List[str])
def get_channels():
    """Get all channels in list form."""
    return channel_list


@app.get("/messages/{channel}", response_model=List[Message])
def get_messages(channel: str):
    """Get all messages for the specified channel."""
    return message_map.get(channel)


@app.post("/post_message", status_code=status.HTTP_201_CREATED)
def post_message(message: Message):
    """Post a new message to the specified channel."""
    channel = message.channel
    if channel in channel_list:
        message_map[channel].append(message)
        return message
    else:
        raise HTTPException(status_code=404, detail="channel not found")
