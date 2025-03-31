import asyncio
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from data.models.meal_request import MealRequest  # Absolute import

router = APIRouter()

@router.post("/recommend-meal", tags=["meal"])
async def recommend_meal(request: Request, meal_request: MealRequest):
    client = request.app.state.client
    assistant_id = request.app.state.assistant_id
    if not assistant_id:
        raise HTTPException(status_code=500, detail="Assistant not initialized")

    try:
        meal_type_str = meal_request.meal_type.value
        thread = client.beta.threads.create()
        message = f"Recommend a {meal_type_str} meal. Preferences: {meal_request.preferences or 'none'}"
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=message)

        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
        while run.status in ["queued", "in_progress"]:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            await asyncio.sleep(1)

        if run.status != "completed":
            raise HTTPException(status_code=500, detail=f"Run failed with status: {run.status}")

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_message = next(m for m in messages.data if m.role == "assistant")
        response_text = assistant_message.content[0].text.value

        # Extract sources from annotations
        sources = []
        if hasattr(assistant_message.content[0].text, 'annotations'):
            for annotation in assistant_message.content[0].text.annotations:
                if annotation.type == "file_citation":
                    file_id = annotation.file_citation.file_id
                    # Get file name from OpenAI API
                    file_info = client.files.retrieve(file_id)
                    sources.append(file_info.filename)

        return {
            "thread_id": thread.id,
            "recommendation": response_text,
            "sources": list(set(sources))  # Remove duplicates
        }
    except HTTPException as e:
        raise e  # Re-raise FastAPI exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing recommendation: {str(e)}")

@router.post("/chat/{thread_id}", tags=["meal"])
async def chat(thread_id: str, request: Request, user_message: str):
    client = request.app.state.client
    assistant_id = request.app.state.assistant_id
    if not assistant_id:
        raise HTTPException(status_code=500, detail="Assistant not initialized")

    try:
        client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_message)
        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

        while run.status in ["queued", "in_progress"]:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            await asyncio.sleep(1)

        if run.status != "completed":
            raise HTTPException(status_code=500, detail=f"Run failed with status: {run.status}")

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_message = next(m for m in messages.data if m.role == "assistant")
        response_text = assistant_message.content[0].text.value

        # Extract sources from annotations
        sources = []
        if hasattr(assistant_message.content[0].text, 'annotations'):
            for annotation in assistant_message.content[0].text.annotations:
                if annotation.type == "file_citation":
                    file_id = annotation.file_citation.file_id
                    file_info = client.files.retrieve(file_id)
                    sources.append(file_info.filename)

        return {
            "response": response_text,
            "sources": list(set(sources))  # Remove duplicates
        }
    except HTTPException as e:
        raise e  # Re-raise FastAPI exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")