import sys
import subprocess
import os

# Define test collections
collections = ["good", "bad1", "bad2", "bad3", "bad4", "bad5", "bad6"]

# Define query tests manually from document structure
query_tests = {
    "good": {
        "1": "What causes climate change?",
        "2": "How does deforestation impact the environment?",
        "3": "What are renewable energy sources?",
        "4": "Why is recycling important?",
        "5": "What are the effects of air pollution?"
    },
    "bad1": {
        "1": "What causes climate change?",
        "2": "How does deforestation impact the environment?",
        "3": "What are renewable energy sources?",
        "4": "Why is recycling important?",
        "5": "What are the effects of air pollution?"
    },
    "bad2": {
        "1": "What causes climate change?",
        "2": "How does deforestation impact the environment?",
        "3": "What are renewable energy sources?",
        "4": "Why is recycling important?",
        "5": "What are the effects of air pollution?"
    },
    "bad3": {},  # Reading issue prevents processing
    "bad4": {},  # Reading issue prevents processing
    "bad5": {
        "1": "What causes climate change?",
        "2": "How does deforestation impact the environment?",
        "3": "What are renewable energy sources?",
        "4": "Why is recycling important?",
        "5": "What are the effects of air pollution?"
    },
    "bad6": {
        "1": "What causes climate change?",
        "2": "How does deforestation impact the environment?",
        "3": "What are renewable energy sources?",
        "4": "Why is recycling important?",
        "5": "What are the effects of air pollution?"
    }
}

program = "./code/print_query.py"

def ensure_processed_queries(collection):
    """
    Ensures the processed query file exists.
    """
    processed_file = f"./processed/{collection}_queries.json"

    if not os.path.exists(processed_file):
        print(f"{collection} ERROR: Processed query file missing, skipping comparison.")
        return False
    return True

# Run tests for all collections
for collection in collections:
    if collection in ["bad3", "bad4"]:
        print(f"{collection} ERROR: Reading issue prevents query processing, skipping.")
        continue

    if not ensure_processed_queries(collection):
        continue

    all_passed = True
    for query_id, expected_output in query_tests.get(collection, {}).items():
        try:
            output = subprocess.check_output(["python3", program, collection, query_id], stderr=subprocess.STDOUT, text=True).strip()
            expected_output = expected_output.strip()
            
            if expected_output != output:
                print(f"{collection} ERROR .Q= {query_id}")
                print(f"Expected: {expected_output}")
                print(f"Got: {output}")
                all_passed = False
        except subprocess.CalledProcessError:
            print(f"{collection} ERROR .Q= {query_id}")
            all_passed = False
    
    if all_passed:
        print(f"{collection} NO ERROR")
