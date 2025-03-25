import asyncio
from fastapi import APIRouter, HTTPException, Request
from openai import OpenAI
from data.models.meal_request import MealRequest  # Absolute import

router = APIRouter()

@router.post("/recommend-meal", tags=["meal"])
async def recommend_meal(request: Request, meal_request: MealRequest):
    client = request.app.state.client  # Get client from app state
    assistant_id = request.app.state.assistant_id
    if not assistant_id:
        raise HTTPException(status_code=500, detail="Assistant not initialized")

    # No manual validation needed; MealType enum enforces valid values
    meal_type_str = meal_request.meal_type.value  # Get the string value from enum

    # Create a thread for the conversation
    thread = client.beta.threads.create()
    message = f"Recommend a {meal_type_str} meal. Preferences: {meal_request.preferences or 'none'}"
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=message)

    # Start the run
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

    # Poll for completion
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        await asyncio.sleep(1)

    if run.status != "completed":
        raise HTTPException(status_code=500, detail=f"Run failed with status: {run.status}")

    # Get the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = next(m.content[0].text.value for m in messages.data if m.role == "assistant")

    return {
        "thread_id": thread.id,  # For follow-up chat
        "recommendation": response
    }

@router.post("/chat/{thread_id}", tags=["meal"])
async def chat(thread_id: str, request: Request, user_message: str):
    client = request.app.state.client  # Get client from app state
    assistant_id = request.app.state.assistant_id
    if not assistant_id:
        raise HTTPException(status_code=500, detail="Assistant not initialized")

    # Add user message to the thread
    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_message)

    # Start a new run
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    # Poll for completion
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        await asyncio.sleep(1)

    if run.status != "completed":
        raise HTTPException(status_code=500, detail=f"Run failed with status: {run.status}")

    # Get the latest assistant response
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = next(m.content[0].text.value for m in messages.data if m.role == "assistant")

    return {"response": response}