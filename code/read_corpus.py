import sys
import os

# Dictionary to store documents using the document ID as the key
documents = {}

def read_corpus(collection):
    '''
    Reads the documents in the collection (inside the 'collections' folder).
    Populates the global `documents` dictionary.
    Detects missing document IDs and missing `.W` sections.
    '''
    corpus_file = f'./collections/{collection}.ALL'

    if not os.path.exists(corpus_file):
        print(f"{collection} ERROR .I=FileNotFound", file=sys.stderr)
        sys.exit(1)

    try:
        with open(corpus_file, 'r') as file:
            doc_id = None
            doc_text = []
            found_ids = set()  # Track document IDs found
            has_w_section = False  # Track if a `.W` section is found

            for line in file:
                line = line.strip()
                if line.startswith('.I'):
                    if doc_id:
                        if not has_w_section or not doc_text:
                            print(f"{collection} ERROR .I={doc_id} .W is Missing", file=sys.stderr)
                            sys.exit(1)
                        documents[doc_id] = ' '.join(doc_text)
                    doc_id = line.split()[1]
                    if not doc_id.isdigit():
                        print(f"{collection} ERROR .I={doc_id} .I is Missing", file=sys.stderr)
                        sys.exit(1)
                    doc_id = int(doc_id)
                    found_ids.add(doc_id)
                    doc_text = []
                    has_w_section = False  # Reset for new document
                elif line.startswith('.W'):
                    has_w_section = True
                else:
                    doc_text.append(line)
            
            # Store the last document
            if doc_id:
                if not has_w_section or not doc_text:
                    print(f"{collection} ERROR .I={doc_id} .W is Missing", file=sys.stderr)
                    sys.exit(1)
                documents[doc_id] = ' '.join(doc_text)

            # Check for missing document IDs
            for i in range(1, max(found_ids) + 1):  # Iterate from 1 to highest ID
                if i not in found_ids:
                    print(f"{collection} ERROR .I={i} .I is Missing", file=sys.stderr)
                    sys.exit(1)

    except Exception as e:
        print(f"{collection} ERROR .I=Exception", file=sys.stderr)
        sys.exit(1)

def write_corpus(collection):
    '''
    Writes the `documents` dictionary to the processed folder
    in a tab-separated format: <docID>\t<docContent>.
    '''
    processed_file = f'./processed/{collection}_document.json'

    try:
        with open(processed_file, 'w') as file:
            for doc_id, doc_content in sorted(documents.items()):
                file.write(f"{doc_id}\t{doc_content}\n")
        print(f"{collection} NO ERROR")
    except Exception as e:
        print(".I=WriteError", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    '''
    Main function
    '''
    if len(sys.argv) != 2:
        print("Usage: python3 read_corpus.py <collection_name>", file=sys.stderr)
        sys.exit(1)

    collection = sys.argv[1]

    read_corpus(collection)
    write_corpus(collection)

    sys.exit(0)
