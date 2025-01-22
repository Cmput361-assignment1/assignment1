import sys
import subprocess
import os

# Define test collections
collections = ["good", "bad1", "bad2", "bad3", "bad4", "bad5", "bad6"]

# Define expected answers manually from document structure
answer_tests = {
    "good": {
        "1": [1],
        "2": [2],
        "3": [3],
        "4": [4],
        "5": [5]
    },
    "bad1": {
        "1": [3, 4],
        "3": [3],
        "4": [4],
        "5": [5]
    },
    "bad2": {
        "1": [1],
        "2": [2],
        "3": [3],
        "4": [4],
        "5": [5]
    },
    "bad3": {
        "1": [1, 2],
        "3": [3],
        "4": [4],
        "5": [5]
    },
    "bad4": {
        "1": [1],
        "2": [2],
        "3": [3],
        "4": [4],
        "5": [5]
    },
    "bad5": {},  # Read failure process
    "bad6": {}   # Read failure process
}

program = "./code/print_answers.py"

def ensure_processed_answers(collection):
    """
    Ensures the processed answers file exists.
    """
    processed_file = f"./processed/{collection}_answers.json"

    if not os.path.exists(processed_file):
        print(f"{collection} ERROR: Processed answers file missing, skipping comparison.")
        return False
    return True

# Run tests for all collections
for collection in collections:
    if collection in ["bad5", "bad6"]:
        print(f"{collection} ERROR: Reading issue prevents answer processing, skipping.")
        continue

    if not ensure_processed_answers(collection):
        continue

    all_passed = True
    for query_id, expected_outputs in answer_tests.get(collection, {}).items():
        try:
            output = subprocess.check_output(["python3", program, collection, query_id], stderr=subprocess.STDOUT, text=True).strip()
            output_values = list(map(int, output.split()))
            
            if sorted(expected_outputs) != sorted(output_values):
                print(f"{collection} ERROR .A= {query_id}")
                print(f"Expected: {expected_outputs}")
                print(f"Got: {output_values}")
                all_passed = False
        except subprocess.CalledProcessError:
            print(f"{collection} ERROR .A= {query_id}")
            all_passed = False
    
    if all_passed:
        print(f"{collection} NO ERROR")
