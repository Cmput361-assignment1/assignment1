import sys
import subprocess
import os

# Define test collections
collections = ["good", "bad1", "bad2", "bad3", "bad4", "bad5", "bad6"]

# Define original document texts manually
original_documents = {
    "good": {
        "1": "Climate change is caused by greenhouse gases.",
        "2": "Deforestation reduces biodiversity and increases CO2 levels.",
        "3": "Renewable energy sources include wind, solar, and hydro.",
        "4": "Recycling helps reduce waste and conserves natural resources.",
        "5": "Air pollution affects human health and the environment."
    },
    "bad3": {
        "1": "Climate change is caused by greenhouse gases.",
        "2": "Deforestation reduces biodiversity and increases CO2 levels.",
        "3": "Renewable energy sources include wind, solar, and hydro.",
        "4": "Recycling helps reduce waste and conserves natural resources.",
        "5": "Air pollution affects human health and the environment."
    },
    "bad4": {
        "1": "Climate change is caused by greenhouse gases.",
        "2": "Deforestation reduces biodiversity and increases CO2 levels.",
        "3": "Renewable energy sources include wind, solar, and hydro.",
        "4": "Recycling helps reduce waste and conserves natural resources.",
        "5": "Air pollution affects human health and the environment."
    },
    "bad5": {
        "1": "Climate change is caused by greenhouse gases.",
        "2": "Deforestation reduces biodiversity and increases CO2 levels.",
        "3": "Renewable energy sources include wind, solar, and hydro.",
        "4": "Recycling helps reduce waste and conserves natural resources.",
        "5": "Air pollution affects human health and the environment."
    },
    "bad6": {
       "1": "Climate change is caused by greenhouse gases.",
        "2": "Deforestation reduces biodiversity and increases CO2 levels.",
        "3": "Renewable energy sources include wind, solar, and hydro.",
        "4": "Recycling helps reduce waste and conserves natural resources.",
        "5": "Air pollution affects human health and the environment."
    }
}

program = "./code/print_document.py"

def ensure_processed_documents(collection):
    """
    Ensures the processed JSON file for documents exists.
    """
    processed_file = f"./processed/{collection}.json"

    if not os.path.exists(processed_file):
        print(f"{collection} ERROR: Processed file missing, skipping comparison.")
        return False
    return True

# Run tests for all collections
for collection in collections:
    if not ensure_processed_documents(collection):
        continue

    all_passed = True
    for doc_id, original_text in original_documents.get(collection, {}).items():
        try:
            output = subprocess.check_output(["python3", program, collection, doc_id], stderr=subprocess.STDOUT, text=True).strip()
            expected_output = original_text.strip()
            
            if expected_output != output:
                print(f"{collection} ERROR .I= {doc_id}")
                print(f"Expected: {expected_output}")
                print(f"Got: {output}")
                all_passed = False
        except subprocess.CalledProcessError:
            print(f"{collection} ERROR .I= {doc_id}")
            all_passed = False
    
    if all_passed:
        print(f"{collection} NO ERROR")
