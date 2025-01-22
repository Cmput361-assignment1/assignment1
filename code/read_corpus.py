import sys
import os
import json

# Dictionary to store documents using the document ID as the key
documents = {}

def read_corpus(collection):
    '''
    Reads the documents in the collection (inside the 'collections' folder).
    Detects missing document IDs, duplicate `.I` entries, and multiple or missing `.W` sections.
    '''
    corpus_file = f'./collections/{collection}.ALL'

    if not os.path.exists(corpus_file):
        print(f"{collection} ERROR .I=FileNotFound", file=sys.stderr)
        sys.exit(1)

    try:
            doc_id = None
            doc_text = []
            found_ids = set()  # Track document IDs found
            has_w_section = False  # Track if a `.W` section is found
            missing_w_errors = []
            multiple_w_errors = []
            duplicate_id_errors = []

            for line in file:
                line = line.strip()
                if line.startswith('.I'):
                    if doc_id:
                        if not has_w_section:
                            print(f"{collection} ERROR .I={doc_id} .W is Missing", file=sys.stderr)
                            sys.exit(1)
                        documents[str(doc_id)] = ' '.join(doc_text)
                    doc_id = line.split()[1]
                    if not doc_id.isdigit():
                        print(f"{collection} ERROR .I={doc_id} Document ID is Invalid", file=sys.stderr)
                        sys.exit(1)
                    doc_id = int(doc_id)
                    if doc_id in found_ids:
                        duplicate_id_errors.append(doc_id)
                    found_ids.add(doc_id)
                    doc_text = []
                    has_w_section = False  # Reset for new document
                elif line.startswith('.W'):
                    if has_w_section:
                        multiple_w_errors.append(doc_id)
                    has_w_section = True
                else:
                    if not has_w_section and doc_id is not None:
                        missing_w_errors.append(doc_id)
                    doc_text.append(line)
            
            # Store the last document
            if doc_id:
                if not has_w_section:
                    print(f"{collection} ERROR .I={doc_id} .W is Missing", file=sys.stderr)
                    sys.exit(1)
                documents[str(doc_id)] = ' '.join(doc_text)

            # Check for missing `.W` sections
            if missing_w_errors:
                for err_id in missing_w_errors:
                    print(f"{collection} ERROR .I={err_id} .W is Missing", file=sys.stderr)
                sys.exit(1)

            # Check for multiple `.W` sections in the same document
            if multiple_w_errors:
                for err_id in multiple_w_errors:
                    print(f"{collection} ERROR .I={err_id+1} Document ID is Missing", file=sys.stderr)
                sys.exit(1)

            # Check for duplicate `.I` document IDs
            if duplicate_id_errors:
                for err_id in duplicate_id_errors:
                    print(f"{collection} ERROR .I={err_id} Duplicate Document ID", file=sys.stderr)
                sys.exit(1)

    except Exception as e:
        print(f"{collection} ERROR .I=Exception", file=sys.stderr)
        sys.exit(1)

def write_corpus(collection):
    '''
    Writes the `documents` dictionary to the processed folder as JSON.
    '''
    processed_file = f'./processed/{collection}.json'

    try:
        with open(processed_file, 'w', encoding='utf-8') as file:
            json.dump(documents, file, indent=4, ensure_ascii=False)  # Save as JSON dictionary
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
