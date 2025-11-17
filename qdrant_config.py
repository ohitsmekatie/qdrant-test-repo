# qdrant_config.py
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import ResponseHandlingException

load_dotenv()  # loads .env from the project root


def get_qdrant_client() -> QdrantClient:
    """Create and return a Qdrant client using env variables."""
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url:
        raise RuntimeError("QDRANT_URL is not set or empty")
    if not api_key:
        raise RuntimeError("QDRANT_API_KEY is not set or empty")

    return QdrantClient(url=url, api_key=api_key)


def health_check(client: QdrantClient) -> None:
    """Print a simple health check showing how many collections exist."""
    try:
        collections = client.get_collections()
        print(f"Connected to Qdrant Cloud: {len(collections.collections)} collections")
    except ResponseHandlingException as e:
        print("Failed to connect to Qdrant:", e)


def create_collection_if_missing(
    client: QdrantClient,
    collection_name: str = "test_collection1",
) -> None:
    """Create a collection if it does not already exist."""
    existing = [c.name for c in client.get_collections().collections]
    if collection_name in existing:
        print(f"Collection '{collection_name}' already exists ✅")
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=4,  # Dimensionality of the vectors
            distance=models.Distance.COSINE,
        ),
    )
    print(f"Created collection '{collection_name}' ✅")

def insert_test_points(client: QdrantClient, collection_name: str) -> None:
    """Insert some throwaway test points into the given collection."""
    points = [
        models.PointStruct(
            id=1,
            vector=[0.1, 0.2, 0.3, 0.4],
            payload={"category": "example"},
        ),
        models.PointStruct(
            id=2,
            vector=[0.2, 0.3, 0.4, 0.5],
            payload={"category": "demo"},
        ),
    ]

    client.upsert(
        collection_name=collection_name,
        points=points,
    )

    print(f"Inserted {len(points)} test points into '{collection_name}' ✅")