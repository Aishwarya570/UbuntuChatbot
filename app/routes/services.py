from fastapi import FastAPI
from pydantic import BaseModel
from utils.chatbot import Chatbot

# Initialize FastAPI and chatbot
app = FastAPI()
chatbot = Chatbot()

# Request model
# class QueryRequest(BaseModel):
#     question: str

@app.post("/ask/{question}")
def ask_question(question : str):
    """Handles question queries and returns chatbot response."""
    response = chatbot.ask(question)
    return {"answer": response.content}

@app.get("/")
def home():
    return {"message": "Chatbot API is running!"}

