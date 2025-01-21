import sys
import json

# Dictionary to store queries
queries = {}

def read_queries(collection):
    '''
    Reads a processed collection (inside the 'processed' folder).
    '''
    global queries
    queries_file = f'./processed/{collection}_queries.json'

    try:
        with open(queries_file, 'r', encoding='utf-8') as f:
            queries = json.load(f)
        # Remove or comment out the debug print statement below
        # print(f"Loaded queries: {list(map(int, queries.keys()))}")
    except FileNotFoundError:
        print(f"Error: Processed file {queries_file} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {queries_file}.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading the file: {e}")
        sys.exit(1)


def retrieve_query(query_id):
    """
    Returns a query given its ID.
    """
    try:
        return queries[query_id]
    except KeyError:
        print(f"Error: Query ID '{query_id}' not found in the collection.")
        sys.exit(1)

if __name__ == "__main__":
    """
    main() function
    """
    # Validate command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 print_query.py <collection> <query_id>")
        sys.exit(1)

    collection = sys.argv[1]
    query_id = sys.argv[2]

    # Validate query ID is an integer
    if not query_id.isdigit():
        print(f"Error: Invalid query ID '{query_id}'. It must be an integer.")
        sys.exit(1)

    # Load queries and retrieve the requested query
    read_queries(collection)
    query = retrieve_query(query_id)

    # Print the query
    print(query)
