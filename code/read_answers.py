'''
Reads answers to queries in the collection file into memory and writes
the data structure to the processed folder.

The program will be run from the root of the repository.
'''

import sys
import os
import json

# Suggestion: keep the answers in a dictionary, using the query ID as the key
answers = {}

def read_answers(collection):
    '''
    Reads the answers in the collection (inside the 'collections' folder).
    '''
    extension = ".REL"  # Correct extension for the CISI.REL file
    answers_file = os.path.join('collections', collection + extension)

    if not os.path.exists(answers_file):
        print(f"Error: File {answers_file} not found.")
        sys.exit(1)

    try:
        with open(answers_file, 'r') as file:
            for line in file:
                parts = line.strip().split()  # Space-separated format
                if len(parts) != 2:
                    continue  # Ignore malformed lines

                query_id = int(parts[0])  # Convert query_id to int
                doc_id = int(parts[1])    # Convert doc_id to int

                if query_id not in answers:
                    answers[query_id] = []
                answers[query_id].append(doc_id)  # Append document ID to the list of answers
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def write_answers(collection):
    '''
    Writes the data structure to the processed folder
    '''
    processed_file = os.path.join('processed', collection + "_answers.json")

    # Ensure the directory exists
    os.makedirs('processed', exist_ok=True)

    try:
        with open(processed_file, 'w') as file:
            json.dump(answers, file, indent=4)  # Save as JSON with proper indentation
        print("SUCCESS")  # Print only if all went well
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    '''
    main() function
    '''
    if len(sys.argv) != 2:
        print("Usage: python read_answers.py <collection_name>")
        sys.exit(1)

    collection_name = sys.argv[1]

    read_answers(collection_name)
    write_answers(collection_name)

    exit(0)
