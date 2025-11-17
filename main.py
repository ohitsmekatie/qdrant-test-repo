# main.py
from qdrant_config import (
    get_qdrant_client,
    health_check,
    create_collection_if_missing,
    insert_test_points,
    search_vectors,
)

def main():
    client = get_qdrant_client()
    health_check(client)
    create_collection_if_missing(client, collection_name="test_collection1")
    insert_test_points(client, collection_name="test_collection1")

    query_vector = [0.08, 0.14, 0.33, 0.28]
    search_vectors(client, "test_collection1", query_vector)


if __name__ == "__main__":
    main()
