'''
Reads all documents in the collection file into memory and writes
the data structure to the processed folder.

The program will be run from the root of the repository.
'''

import sys
import os

# Suggestion: keep the documents in a dictionary, using the ID as the key
documents = {}

def read_documents(collection):
    '''
    Reads the documents in the collection (inside the 'collections' folder).
    Populates the global `documents` dictionary.
    '''
    corpus_file = f'./collections/{collection}.ALL'

    if not os.path.exists(corpus_file):
        print(f"Error: Collection file {corpus_file} not found.")
        sys.exit(1)

    try:
        with open(corpus_file, 'r') as file:
            doc_id = None
            doc_text = []
            for line in file:
                line = line.strip()
                if line.startswith('.I'):
                    if doc_id:
                        documents[doc_id] = ' '.join(doc_text)
                    doc_id = int(line.split()[1])
                    doc_text = []
                elif line.startswith('.W'):
                    continue
                else:
                    doc_text.append(line)
            if doc_id:
                documents[doc_id] = ' '.join(doc_text)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def write_documents(collection):
    '''
    Writes the `documents` dictionary to the processed folder
    in a tab-separated format: <docID>\t<docContent>.
    '''
    processed_file = f'./processed/{collection}_document.json'

    # Check if processed file already exists
    if os.path.exists(processed_file):
        print(f"Error: Processed file {processed_file} already exists.")
        sys.exit(1)

    try:
        with open(processed_file, 'w') as file:
            for doc_id, doc_content in documents.items():
                file.write(f"{doc_id}\t{doc_content}\n")
        print("SUCCESS")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    '''
    main() function
    '''
    # Check for the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python3 read_corpus.py <collection_name>")
        sys.exit(1)

    # Read the collection name from command line
    collection = sys.argv[1]

    # Read and process the documents
    read_documents(collection)

    # Write the processed data to the processed folder
    write_documents(collection)

    sys.exit(0)
