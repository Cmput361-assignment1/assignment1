import sys
import os
import json

# Dictionary to store queries using the query ID as the key
queries = {}

def read_queries(collection):
    '''
    Reads the queries in the collection (inside the 'collections' folder).
    Detects missing query IDs, duplicate `.I` entries, and multiple or missing `.W` sections.
    '''
    queries_file = f'./collections/{collection}.QRY'

    if not os.path.exists(queries_file):
        print(f"{collection} ERROR .I=FileNotFound", file=sys.stderr)
        sys.exit(1)

    try:
        with open(queries_file, 'r', encoding='utf-8') as file:
            query_id = None
            query_text = []
            found_ids = set()  # Track query IDs found
            has_w_section = False  # Track if a `.W` section is found
            missing_w_errors = []
            multiple_w_errors = []
            duplicate_id_errors = []

            for line in file:
                line = line.strip()
                if line.startswith('.I'):
                    if query_id:
                        if not has_w_section:
                            print(f"{collection} ERROR .I={query_id} .W is Missing", file=sys.stderr)
                            sys.exit(1)
                        queries[str(query_id)] = ' '.join(query_text)
                    query_id = line.split()[1]
                    if not query_id.isdigit():
                        print(f"{collection} ERROR .I={query_id} Query ID is Invalid", file=sys.stderr)
                        sys.exit(1)
                    query_id = int(query_id)
                    if query_id in found_ids:
                        duplicate_id_errors.append(query_id)
                    found_ids.add(query_id)
                    query_text = []
                    has_w_section = False  # Reset for new query
                elif line.startswith('.W'):
                    if has_w_section:
                        multiple_w_errors.append(query_id)
                    has_w_section = True
                else:
                    if not has_w_section and query_id is not None:
                        missing_w_errors.append(query_id)
                    query_text.append(line)
            
            # Store the last query
            if query_id:
                if not has_w_section:
                    print(f"{collection} ERROR .I={query_id} .W is Missing", file=sys.stderr)
                    sys.exit(1)
                queries[str(query_id)] = ' '.join(query_text)

            # Check for missing `.W` sections
            if missing_w_errors:
                for err_id in missing_w_errors:
                    print(f"{collection} ERROR .I={err_id} .W is Missing", file=sys.stderr)
                sys.exit(1)

            # Check for multiple `.W` sections in the same query
            if multiple_w_errors:
                for err_id in multiple_w_errors:
                    print(f"{collection} ERROR .I={err_id} Query ID is Missing", file=sys.stderr)
                sys.exit(1)

            # Check for duplicate `.I` query IDs
            if duplicate_id_errors:
                for err_id in duplicate_id_errors:
                    print(f"{collection} ERROR .I={err_id} Duplicate Query ID", file=sys.stderr)
                sys.exit(1)

    except Exception as e:
        print(f"{collection} ERROR .I=Exception", file=sys.stderr)
        sys.exit(1)

def write_queries(collection):
    '''
    Writes the `queries` dictionary to the processed folder as JSON.
    '''
    processed_file = f'./processed/{collection}_queries.json'

    try:
        with open(processed_file, 'w', encoding='utf-8') as file:
            json.dump(queries, file, indent=4, ensure_ascii=False)  # Save as JSON dictionary
        print(f"{collection} NO ERROR")
    except Exception as e:
        print(".I=WriteError", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    '''
    Main function
    '''
    if len(sys.argv) != 2:
        print("Usage: python3 read_queries.py <collection_name>", file=sys.stderr)
        sys.exit(1)

    collection = sys.argv[1]

    read_queries(collection)
    write_queries(collection)

    sys.exit(0)
