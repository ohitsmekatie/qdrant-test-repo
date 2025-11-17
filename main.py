# main.py
from qdrant_config import (
    get_qdrant_client,
    health_check,
    create_collection_if_missing,
    insert_test_points,
)

def main():
    client = get_qdrant_client()
    health_check(client)
    create_collection_if_missing(client, collection_name="test_collection1")
    insert_test_points(client, collection_name="test_collection1")


if __name__ == "__main__":
    main()
