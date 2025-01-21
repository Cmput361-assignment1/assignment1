'''
Prints the *contents* of a document, as in the corpus, but read from 
a processed file.

The program will be run from the root of the repository.
'''

import sys
import os


# Suggestion: keep the documents in a dictionary, using the ID as the key
documents = {}

def read_documents(collection):
    '''
    Reads a processed collection (inside the 'processed' folder).
    Populates the global `documents` dictionary.
    '''
    corpus_file = f'./processed/{collection}.json'

    if not os.path.exists(corpus_file):
        print(f"Error: Processed file {corpus_file} not found.")
        sys.exit(1)

    try:
        with open(corpus_file, 'r') as file:
            for line in file:
                doc_id, doc_content = line.strip().split('\t', 1)
                documents[int(doc_id)] = doc_content.strip()
    except FileNotFoundError:
        print(f"Error: File {corpus_file} not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Malformed line in processed file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def retrieve_document(docID):
    '''
    Returns a document given its id.
    Throws an error if the document ID is not found.
    '''
    if docID not in documents:
        print(f"Error: Document ID {docID} not found.")
        sys.exit(1)

    return documents[docID]

if __name__ == "__main__":
    '''
    main() function
    '''
    # Check for the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python3 print_document.py <collection_name> <document_id>")
        sys.exit(1)

    # Read command-line arguments
    collection = sys.argv[1]
    try:
        doc_id = int(sys.argv[2])
    except ValueError:
        print("Error: Document ID must be an integer.")
        sys.exit(1)

    # Read the processed documents
    read_documents(collection)

    # Retrieve and print the document
    document = retrieve_document(doc_id)
    print(document)

    sys.exit(0)
