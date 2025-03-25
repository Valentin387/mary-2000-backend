import os
from fastapi import FastAPI
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Configure CORS settings
origins = [
  "http://localhost", # Add the URL of your Angular frontend
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allow_headers=["Authorization", "Content-Type"]
)

from routers import meal_recommendation
app.include_router(meal_recommendation.router)

client = OpenAI()

from services import fileUploader

def setup_assistant():
  vector_store_id = fileUploader.set_up_vector_store()
  assistants = client.beta.assistants.list()
  if not any(a.name == "MealRecommender" for a in assistants.data):
      assistant = client.beta.assistants.create(
          name="MealRecommender",
          instructions="You are a meal recommendation assistant. Use the provided meal plans from the vector store to suggest meals based on the user's requested meal type and any additional preferences. Provide a detailed response including the meal description, ingredients, and cooking notes if available. If no exact match is found, suggest a close alternative and explain why.",
          model="gpt-4o-mini",
          tools=[{"type": "file_search"}],
          tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
      )
      print(f"Created assistant with ID: {assistant.id}")
      return assistant.id
  else:
      assistant = next(a for a in assistants.data if a.name == "MealRecommender")
      client.beta.assistants.update(
          assistant_id=assistant.id,
          tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
      )
      print(f"Updated assistant with ID: {assistant.id}")
      return assistant.id

app.state.assistant_id = None

async def startup_event():
  app.state.assistant_id = setup_assistant()

app.add_event_handler("startup", startup_event)

@ app.get("/")
async def root():
  return {"message": "Meal Recommendation API is running"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)