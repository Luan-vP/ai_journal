import pytest

from ai_journal.storage import upload_text_to_weaviate_collection, WEAVIATE_COLLECTION_NAME

from conftest import test_weaviate_client

def test_upload_text_to_weaviate_collection(test_weaviate_client):

    collection = test_weaviate_client.collections.get(WEAVIATE_COLLECTION_NAME)
    response = collection.query.near_text(
        query="any random query",
        limit=10,
        # return_metadata=MetadataQuery(distance=True)
    )

    assert len(response.objects) == 0

    upload_text_to_weaviate_collection("mango is my favourite fruit", test_weaviate_client)

    response = collection.query.near_text(
        query="any random query",
        limit=10,
        # return_metadata=MetadataQuery(distance=True)
    )

    assert len(response.objects) == 1

    upload_text_to_weaviate_collection("pineapple is my new favourite fruit!", test_weaviate_client)

    response = collection.query.near_text(
        query="any random query",
        limit=10,
        # return_metadata=MetadataQuery(distance=True)
    )

    assert len(response.objects) == 2