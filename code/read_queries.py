import os
import json
import sys

# Dictionary to hold query data
queries = {}

def read_queries(collection):
    """
    Reads the queries in the collection (inside the 'collections' folder).
    Detects missing query IDs and missing `.W` sections.
    """
    input_file = f'./collections/{collection}.QRY'
    
    if not os.path.exists(input_file):
        print(f"{collection} ERROR .I=FileNotFound", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            query_id = None
            query_text = []
            found_ids = set()
            has_w_section = False  # Track if `.W` section exists

            for line in file:
                line = line.strip()
                if line.startswith(".I"):
                    # Save the previous query if it exists
                    if query_id is not None:
                        if not has_w_section or not query_text:
                            print(f"{collection} ERROR .I={query_id} .W is Missing", file=sys.stderr)
                            sys.exit(1)
                        queries[query_id] = ' '.join(query_text).strip()
                    # Start a new query
                    try:
                        query_id = int(line.split()[1])
                    except ValueError:
                        print(f"{collection} ERROR .I=MalformedID", file=sys.stderr)
                        sys.exit(1)
                    found_ids.add(query_id)
                    query_text = []
                    has_w_section = False  # Reset for new query
                elif line.startswith(".W"):
                    has_w_section = True
                else:
                    # Collect query text
                    query_text.append(line)
            
            # Save the last query
            if query_id is not None:
                if not has_w_section or not query_text:
                    print(f"{collection} ERROR .I={query_id} .W is Missing", file=sys.stderr)
                    sys.exit(1)
                queries[query_id] = ' '.join(query_text).strip()

            # Check for missing query IDs
            for i in range(1, max(found_ids) + 1):
                if i not in found_ids:
                    print(f"{collection} ERROR .I={i} .I is Missing", file=sys.stderr)
                    sys.exit(1)

    except Exception as e:
        print(f"{collection} ERROR .I=Exception", file=sys.stderr)
        sys.exit(1)

def write_queries(collection):
    """
    Writes the queries dictionary to a JSON file in the 'processed' folder.
    """
    output_file = f'./processed/{collection}_queries.json'
    
    # Ensure the processed folder exists
    os.makedirs('./processed', exist_ok=True)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(queries, file, indent=4, ensure_ascii=False)
        print(f"{collection} NO ERROR")
    except Exception as e:
        print(f"{collection} ERROR .I=WriteError", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 read_queries.py <collection>", file=sys.stderr)
        sys.exit(1)
    
    collection = sys.argv[1]
    read_queries(collection)
    write_queries(collection)
    sys.exit(0)
