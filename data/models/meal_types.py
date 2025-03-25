from enum import Enum

class MealType(str, Enum):
    DESAYUNO = "desayuno"
    ALMUERZO = "almuerzo"
    CENA = "cena"
    POSTRE = "postre"
    SALSA = "salsa"
    SNACK = "snack"
    SURPRISE = "surprise"  # Added for the "Surprise" option