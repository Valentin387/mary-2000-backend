from pydantic import BaseModel
from .meal_types import MealType

# Request model for meal recommendation
class MealRequest(BaseModel):
    meal_type: MealType
    preferences: str = ""  # Optional user preferences (e.g., "high protein", "vegetarian")