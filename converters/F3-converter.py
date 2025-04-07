import csv
import os
from pathlib import Path

# Define project root directory (two levels up from this script)
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'data', 'txt exports')

def convert_csv_to_txt(csv_file: str, output_dir: str = OUTPUT_DIR):
    """
    Convert a well-formatted CSV file to meal-type-specific .txt files.
    
    Args:
        csv_file (str): Path to the input CSV file.
        output_dir (str): Directory to save the output .txt files (defaults to OUTPUT_DIR).
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Dictionary to store meals by type
    meals_by_type = {}

    # Read CSV file
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Verify expected columns
        expected_columns = {
            'Date', 'Meal Type', 'Protein', 'Dairy', 'Carbohydrates', 
            'Vegetables', 'Fruits', 'Fats', 'Beverage', 'Dessert', 
            'Plating', 'Cooking Notes'
        }
        if set(reader.fieldnames) != expected_columns:
            raise ValueError(f"CSV columns mismatch. Expected: {expected_columns}, Got: {reader.fieldnames}")

        # Group rows by Meal Type
        for row in reader:
            meal_type = row['Meal Type'].lower().strip()  # Normalize (e.g., "Desayuno" -> "desayuno")
            if meal_type not in meals_by_type:
                meals_by_type[meal_type] = []
            meals_by_type[meal_type].append(row)

    # Write to .txt files
    for meal_type, meals in meals_by_type.items():
        output_file = os.path.join(output_dir, f"{meal_type}.txt")
        with open(output_file, 'w', encoding='utf-8') as txtfile:
            for i, meal in enumerate(meals, 1):
                txtfile.write(f"Meal Entry {i} ({meal['Date']}):\n")
                txtfile.write(f"  Meal Type: {meal['Meal Type']}\n")
                txtfile.write(f"  Protein: {meal['Protein']}\n")
                txtfile.write(f"  Dairy: {meal['Dairy']}\n")
                txtfile.write(f"  Carbohydrates: {meal['Carbohydrates']}\n")
                txtfile.write(f"  Vegetables: {meal['Vegetables']}\n")
                txtfile.write(f"  Fruits: {meal['Fruits']}\n")
                txtfile.write(f"  Fats: {meal['Fats']}\n")
                txtfile.write(f"  Beverage: {meal['Beverage']}\n")
                txtfile.write(f"  Dessert: {meal['Dessert']}\n")
                txtfile.write(f"  Plating: {meal['Plating']}\n")
                txtfile.write(f"  Cooking Notes: {meal['Cooking Notes']}\n")
                txtfile.write("\n")  # Blank line between entries

    print(f"Converted {csv_file} to .txt files in {output_dir}")

if __name__ == "__main__":
    # Example usage with a specific input file
    INPUT_CSV = os.path.join(PROJECT_DIR, 'data', 'csv exports', 'Daily Meals Tracker Template - F3.csv')
    convert_csv_to_txt(INPUT_CSV)