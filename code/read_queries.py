import os
import json

# Dictionary to hold query data
queries = {}

def read_queries(collection):
    """
    Reads the queries in the collection (inside the 'collections' folder).
    """
    input_file = f'./collections/{collection}.qry'
    
    if not os.path.exists(input_file):
        print(f"Error: Collection file {input_file} not found.")
        exit(1)
    
    print(f"Reading queries from {input_file}")
    with open(input_file, 'r', encoding='utf-8') as file:
        query_id = None
        query_text = []

        for line in file:
            line = line.strip()
            if line.startswith(".I"):
                # Save the previous query if it exists
                if query_id is not None:
                    queries[query_id] = ' '.join(query_text).strip()
                # Start a new query
                try:
                    query_id = int(line.split()[1])
                except ValueError:
                    print(f"Error: Malformed query ID line: {line}")
                    exit(1)
                query_text = []
            elif line.startswith(".W"):
                # Begin capturing query text
                continue
            else:
                # Collect query text
                query_text.append(line)
        
        # Save the last query
        if query_id is not None:
            queries[query_id] = ' '.join(query_text).strip()
    print(f"Loaded {len(queries)} queries.")


def write_queries(collection):
    """
    Writes the queries dictionary to a JSON file in the 'processed' folder.
    """
    output_file = f'./processed/{collection}_queries.json'
    
    # Ensure the processed folder exists
    os.makedirs('./processed', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(queries, file, indent=4, ensure_ascii=False)
        print(f"Saved queries to {output_file}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 read_queries.py <collection>")
        exit(1)
    
    collection = sys.argv[1]
    read_queries(collection)
    write_queries(collection)
    print("SUCCESS")
