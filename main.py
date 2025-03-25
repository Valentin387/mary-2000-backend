import os
from fastapi import FastAPI
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = OpenAI()

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

from routers import meal_recommendation # Absolute import
app.include_router(meal_recommendation.router)

from services.fileUploader import set_up_vector_store

def setup_assistant():
  vector_store_id = set_up_vector_store()
  assistants = client.beta.assistants.list()
  assistant_name = "GrandmasMealAssistant"
  if not any(a.name == assistant_name for a in assistants.data):
      assistant = client.beta.assistants.create(
          name=assistant_name,
          instructions="You are a meal recommendation assistant based on my grandmother's cooking. Use the provided meal data to suggest meals based on the user's meal type (desayuno, almuerzo, cena, snack, postre, salsa, surprise) and preferences. Include meal description, ingredients, and cooking notes. For 'surprise', pick a random meal type from desayuno, almuerzo, cena, or snack. If no exact match exists, suggest a close alternative with reasoning.",
          model="gpt-4o-mini",
          tools=[{"type": "file_search"}],
          tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
      )
      print(f"Created assistant with ID: {assistant.id}")
      return assistant.id
  else:
      assistant = next(a for a in assistants.data if a.name == assistant_name)
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
  return {"message": "Grandma's Meal Recommendation API is running"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run('main:app', port=8000, reload=True)