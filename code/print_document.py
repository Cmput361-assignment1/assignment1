import sys
import os
import json

# Dictionary to store documents using the document ID as the key
documents = {}

def read_documents(collection):
    '''
    Reads a processed collection (inside the 'processed' folder).
    Populates the global `documents` dictionary.
    '''
    corpus_file = f'./processed/{collection}.json'

    if not os.path.exists(corpus_file):
        print(f"Error: Processed file {corpus_file} not found.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(corpus_file, 'r', encoding='utf-8') as file:
            global documents
            documents = json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Malformed JSON in processed file {corpus_file}.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def retrieve_document(docID):
    '''
    Returns a document given its id.
    Throws an error if the document ID is not found.
    '''
    docID = str(docID)  # Ensure docID is a string for JSON lookup
    if docID not in documents:
        print(f"Error: Document ID {docID} not found.", file=sys.stderr)
        sys.exit(1)

    return documents[docID]

if __name__ == "__main__":
    '''
    main() function
    '''
    if len(sys.argv) != 3:
        print("Usage: python3 print_document.py <collection_name> <document_id>", file=sys.stderr)
        sys.exit(1)

    # Read command-line arguments
    collection = sys.argv[1]
    try:
        doc_id = int(sys.argv[2])
    except ValueError:
        print("Error: Document ID must be an integer.", file=sys.stderr)
        sys.exit(1)

    # Read the processed documents
    read_documents(collection)

    # Retrieve and print the document
    document = retrieve_document(doc_id)
    print(document)

    sys.exit(0)
