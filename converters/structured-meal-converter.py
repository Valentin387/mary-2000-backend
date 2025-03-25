import os
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime

# Define the absolute path to the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'data', 'txt exports')

# Input files
INPUT_FILES = [
    os.path.join(PROJECT_DIR, 'data', 'csv exports', 'Daily Meals Tracker Template - 2025.csv'),
    os.path.join(PROJECT_DIR, 'data', 'csv exports', 'Daily Meals Tracker Template - Structured Form Legacy.csv')
]

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to normalize date to DD/MM/YYYY format
def normalize_date(date_str):
    if not date_str:
        return 'Unknown'
    try:
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d'):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%d/%m/%Y')
            except ValueError:
                continue
        raise ValueError(f"Unknown date format: {date_str}")
    except ValueError as e:
        print(f"Warning: {e}. Defaulting to 'Unknown'")
        return 'Unknown'

# Function to parse the CSV using csv module
def parse_meal_entries(csv_path):
    meals = []
    current_meal = {}
    food_groups = {}

    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        in_food_groups = False

        for row in reader:
            if not row or all(x.strip() == '' for x in row):
                continue

            key = row[0].strip()
            value = row[1].strip() if len(row) > 1 else ''

            if key == 'Daily Meals Tracker Template':
                if current_meal:  # Save the previous meal
                    if food_groups:
                        current_meal['Food Groups'] = food_groups
                    meals.append(current_meal)
                    food_groups = {}
                current_meal = {}
                in_food_groups = False
                continue

            if key == 'Food Groups':
                in_food_groups = True
                continue

            if key == 'Date' and value:
                value = normalize_date(value)

            if in_food_groups and value:
                food_groups[key] = value
            elif value:  # Only add non-empty values outside Food Groups
                current_meal[key] = value

        # Append the last meal
        if current_meal:
            if food_groups:
                current_meal['Food Groups'] = food_groups
            meals.append(current_meal)

    return meals

# Function to format a meal entry, excluding empty fields
def format_meal_entry(row):
    # Define fields to check
    fields = {
        'Date': str(row.get('Date', 'Unknown')),
        'Protein': str(row.get('Protein', 'None')),
        'Dairy': str(row.get('Dairy', 'None')),
        'Carbohydrates': str(row.get('Carbohydrates', 'None')),
        'Vegetables': str(row.get('Vegetables', 'None')),
        'Fruits': str(row.get('Fruits', 'None')),
        'Fats': str(row.get('Fats', 'None')),
        'Beverage': str(row.get('Beverage', 'None')),
        'Dessert': str(row.get('Dessert', 'None')),
        'Plating': str(row.get('Plating', 'None')),
        'Cooking Notes': str(row.get('Cooking Notes', 'None'))
    }

    # Filter out empty or null fields
    non_empty_fields = {k: v for k, v in fields.items() if v and v.lower() not in ('', 'none', 'nan')}

    # Build the formatted string
    lines = [f"**{row['Meal Type']} Meal on {non_empty_fields.pop('Date', 'Unknown')}**"]
    for field_name, field_value in non_empty_fields.items():
        if field_name == 'Cooking Notes':
            lines.append(f"- {field_name}: \n{field_value}")
        else:
            lines.append(f"- {field_name}: {field_value}")

    return '\n'.join(lines)

# Process each input file
meal_types = ['desayuno', 'almuerzo', 'cena', 'salsa', 'postre', 'snack']

for csv_file in INPUT_FILES:
    # Parse the CSV into a list of meal dictionaries
    meal_entries = parse_meal_entries(csv_file)
    print(f"Parsed meal entries from {csv_file}:", meal_entries)

    # Flatten the meal entries to merge Food Groups into top-level fields
    flattened_meals = []
    for meal in meal_entries:
        flattened_meal = meal.copy()
        food_groups = flattened_meal.pop('Food Groups', {})
        flattened_meal.update(food_groups)
        flattened_meals.append(flattened_meal)

    # Convert to DataFrame
    df = pd.DataFrame(flattened_meals)
    print(f"Converted to DataFrame from {csv_file}:\n", df)

    # Append to existing text files for each meal type
    for meal_type in meal_types:
        meal_df = df[df['Meal Type'] == meal_type]
        output_file = os.path.join(OUTPUT_DIR, f'{meal_type.lower()}.txt')
        with open(output_file, 'a', encoding='utf-8') as f:  # Append mode
            for index, row in meal_df.iterrows():
                formatted_entry = format_meal_entry(row)
                f.write(formatted_entry)
                f.write('\n\n')

print("Text files updated with meal entries in", OUTPUT_DIR)