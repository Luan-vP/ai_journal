import pytest

from ai_journal.storage import upload_text_to_weaviate_collection, WEAVIATE_COLLECTION_NAME

from conftest import test_weaviate_client

def test_upload_text_to_weaviate_collection(test_weaviate_client):

    # TODO
    # test no matches for vector search on "mango"
    collection = test_weaviate_client.collections.get(WEAVIATE_COLLECTION_NAME)
    response = collection.query.near_text(
        query="animals in movies",
        limit=1,
        # return_metadata=MetadataQuery(distance=True)
    )

    assert len(response.objects) == 0
    

    upload_text_to_weaviate_collection("mango is my favourite fruit", test_weaviate_client)

    # TODO
    # Test there is now a match for "mango"

    response = collection.query.near_text(
        query="animals in movies",
        limit=1,
        # return_metadata=MetadataQuery(distance=True)
    )

    assert len(response.objects) == 1