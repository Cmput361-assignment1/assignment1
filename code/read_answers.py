import sys
import os
import json

# Dictionary to store answers using query ID as the key
answers = {}

def read_answers(collection):
    '''
    Reads the answers in the collection (inside the 'collections' folder) and checks for consistency.
    '''
    extension = ".REL"  # Correct extension for the CISI.REL file
    answers_file = os.path.join('collections', collection + extension)
    queries_file = os.path.join('collections', collection + ".QRY")
    documents_file = os.path.join('collections', collection + ".ALL")

    if not os.path.exists(answers_file):
        print(f"{collection} ERROR .I=FileNotFound", file=sys.stderr)
        sys.exit(1)

    # Collect valid query and document IDs for validation
    valid_queries = set()
    valid_documents = set()

    try:
        with open(queries_file, 'r') as file:
            for line in file:
                if line.startswith(".I"):
                    valid_queries.add(int(line.split()[1]))
    except Exception as e:
        print(f"{collection} ERROR .I is MissingQRY", file=sys.stderr)
        sys.exit(1)

    try:
        with open(documents_file, 'r') as file:
            for line in file:
                if line.startswith(".I"):
                    valid_documents.add(int(line.split()[1]))
    except Exception as e:
        print(f"{collection} ERROR .I is MissingALL", file=sys.stderr)
        sys.exit(1)

    try:
        with open(answers_file, 'r') as file:
            for line in file:
                parts = line.strip().split()  # Space-separated format
                if len(parts) != 2:
                    continue  # Ignore malformed lines

                query_id = int(parts[0])  # Convert query_id to int
                doc_id = int(parts[1])    # Convert doc_id to int

                # Check if the query ID exists in .QRY
                if query_id not in valid_queries:
                    print(f"{collection} ERROR .I={query_id} NotFound in {collection}.QRL", file=sys.stderr)
                    sys.exit(1)

                # Check if the document ID exists in .ALL
                if doc_id not in valid_documents:
                    print(f"{collection} ERROR .I={doc_id} NotFound in {collection}.ALL", file=sys.stderr)
                    sys.exit(1)

                if query_id not in answers:
                    answers[query_id] = []
                answers[query_id].append(doc_id)  # Append document ID to the list of answers
    except Exception as e:
        print(f"{collection} ERROR .I ReadError", file=sys.stderr)
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
        print(f"{collection} NO ERROR")  # Print only if all went well
    except Exception as e:
        print(f"{collection} ERROR .I WriteError", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    '''
    main() function
    '''
    if len(sys.argv) != 2:
        print("Usage: python read_answers.py <collection_name>", file=sys.stderr)
        sys.exit(1)

    collection_name = sys.argv[1]

    read_answers(collection_name)
    write_answers(collection_name)

    exit(0)
