'''
Prints the *answers* to a query, as in the collection file, but read from 
a processed file. 
Answers are document IDs and should be printed one per line.

The program will be run from the root of the repository.
'''

import sys
import os
import json

# Dictionary to store answers
answers = {}

def read_answers(collection):
    '''
    Reads a processed collection (inside the 'processed' folder).
    '''
    answers_file = f'./processed/{collection}_answers.json'

    if not os.path.exists(answers_file):
        print(f"Error: Processed file {answers_file} not found.")
        sys.exit(1)

    try:
        with open(answers_file, 'r') as file:
            global answers
            answers = json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {answers_file}.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def retrieve_answers_to_query(query_id):
    '''
    Returns the answers to a query given its ID
    '''
    try:
        query_id = str(query_id)  # Ensure the query ID is a string
        if query_id not in answers:
            raise KeyError(f"Query ID {query_id} not found.")
        return answers[query_id]
    except KeyError:
        print(f"Error: Query ID {query_id} not found.")
        sys.exit(1)


if __name__ == "__main__":
    '''
    main() function
    '''
    if len(sys.argv) != 3:
        print("Usage: python3 print_answers.py <collection_name> <query_id>")
        sys.exit(1)

    collection = sys.argv[1]
    query_id = sys.argv[2]

    # Validate query ID
    if not query_id.isdigit():
        print(f"Error: Query ID {query_id} is not valid. It must be an integer.")
        sys.exit(1)

    # Read the processed answers and retrieve the answer for the query
    read_answers(collection)
    answers_to_query = retrieve_answers_to_query(query_id)

    # Print the answers, one per line
    for answer in answers_to_query:
        print(answer)
