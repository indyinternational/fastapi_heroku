from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
import requests
import json

# Instantiate the FastAPI
app = FastAPI()

# In a real app, we would have a database.
# But, let's keep it super simple for now!
channel_list = ["general", "dev", "marketing"]
message_map = {}
for channel in channel_list:
    message_map[channel] = []

@app.get("/1")
def get_status():
    """Get status of messaging server."""
    response_API = requests.get('http://indyinter.duckdns.org:8081/authen/zero/1234')
    data = response_API.text
    parse_json = json.loads(data)
    return parse_json

