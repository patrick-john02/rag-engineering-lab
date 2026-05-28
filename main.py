from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel
import logfire
from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app:FastAPI):
    logfire.instrument_fastapi
    yield

#initiate the app (fastapi)
app = FastAPI(title="Rag Engineering Lab Practice")

load_dotenv()
logfire.configure()


class ChatRequest(BaseModel):
    prompt: str
    

@app.get('/')
async def root():
    return {"message": "Chatbot is running"}

@app.post('/chat')
async def chat(request:ChatRequest):
    async def stream_text():
        input_state = {"messages": [("user", request.prompt)]}
        
        # async for update in 
    