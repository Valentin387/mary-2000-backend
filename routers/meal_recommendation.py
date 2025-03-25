from fastapi import APIRouter, HTTPException, Request
from openai import OpenAI
from ..data.models.meal_request import MealRequest
import asyncio
from data.models.meal_types import MealType

router = APIRouter()
client = OpenAI()

@router.post("/recommend-meal", tags=["meal"])
async def recommend_meal(request: Request, meal_request: MealRequest):
    assistant_id = request.app.state.assistant_id
    if not assistant_id:
        raise HTTPException(status_code=500, detail="Assistant not set up")

    # No need for manual validation; MealRequest already enforces MealType
    
    thread = client.beta.threads.create()
    message = f"Recommend a {meal_request.meal_type} meal. Preferences: {meal_request.preferences or 'none'}"
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=message)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        await asyncio.sleep(1)

    if run.status != "completed":
        raise HTTPException(status_code=500, detail=f"Run failed with status: {run.status}")

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = next(m.content[0].text.value for m in messages.data if m.role == "assistant")

    return {"recommendation": response}