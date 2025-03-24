import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# Define the absolute path to the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
MEAL_ENTRIES_CSV = os.path.join(PROJECT_DIR, 'data', 'csv exports', 'Daily Meals Tracker Template - 2025.csv')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'data', 'txt exports')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to normalize date to DD/MM/YYYY format
def normalize_date(date_str):
    if not date_str:
        return None
    try:
        # Try parsing common date formats
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d'):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%d/%m/%Y')
            except ValueError:
                continue
        raise ValueError(f"Unknown date format: {date_str}")
    except ValueError as e:
        print(f"Warning: {e}. Defaulting to original string: {date_str}")
        return date_str  # Fallback to original if parsing fails

# Function to parse the CSV into a list of meal dictionaries
def parse_meal_entries(csv_path):
    meals = []
    current_meal = {}
    food_groups = {}
    in_food_groups = False

    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith(','):
            continue

        if line.startswith('Daily Meals Tracker Template'):
            if current_meal:  # Save the previous meal if it exists
                if food_groups:
                    current_meal['Food Groups'] = food_groups
                meals.append(current_meal)
                food_groups = {}
            current_meal = {}
            in_food_groups = False
            continue

        if line.startswith('Food Groups'):
            in_food_groups = True
            continue

        if ',' not in line:
            continue

        key, value = [x.strip() for x in line.split(',', 1)]
        if value == '':
            value = None

        if key == 'Date' and value:
            value = normalize_date(value)  # Normalize the date

        if in_food_groups:
            food_groups[key] = value
        else:
            current_meal[key] = value

    # Append the last meal
    if current_meal:
        if food_groups:
            current_meal['Food Groups'] = food_groups
        meals.append(current_meal)

    return meals

# Parse the CSV into a list of meal dictionaries
meal_entries = parse_meal_entries(MEAL_ENTRIES_CSV)
#print("Parsed meal entries:", meal_entries)

# Flatten the meal entries to merge Food Groups into top-level fields
flattened_meals = []
for meal in meal_entries:
    flattened_meal = meal.copy()  # Copy the original meal dict
    food_groups = flattened_meal.pop('Food Groups', {})  # Remove and get Food Groups
    flattened_meal.update(food_groups)  # Merge Food Groups fields into the top-level dict
    flattened_meals.append(flattened_meal)

# Convert to DataFrame
df = pd.DataFrame(flattened_meals)
#print("Converted to DataFrame:\n", df)

# Define meal types
meal_types = ['desayuno', 'almuerzo', 'cena', 'snack']

# Function to format a meal entry into a readable text block
def format_meal_entry(row):
    return f"""**{row['Meal Type']} Meal on {row['Date']}**
- Protein: {row.get('Protein', 'None')}
- Dairy: {row.get('Dairy', 'None')}
- Carbohydrates: {row.get('Carbohydrates', 'None')}
- Vegetables: {row.get('Vegetables', 'None')}
- Fruits: {row.get('Fruits', 'None')}
- Fats: {row.get('Fats', 'None')}
- Beverage: {row.get('Beverage', 'None')}
- Dessert: {row.get('Dessert', 'None')}
- Plating: {row.get('Plating', 'None')}
- Cooking Notes: {row.get('Cooking Notes', 'None')}
"""

# Process each meal type and write to a separate file
for meal_type in meal_types:
    # Filter rows for the current meal type
    meal_df = df[df['Meal Type'] == meal_type]

    # Create a text file for the meal type in the txt exports folder
    output_file = os.path.join(OUTPUT_DIR, f'{meal_type.lower()}.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for index, row in meal_df.iterrows():
            f.write(format_meal_entry(row))
            f.write('\n\n')  # Add spacing between entries

print("Text files created for meal entries in", OUTPUT_DIR)