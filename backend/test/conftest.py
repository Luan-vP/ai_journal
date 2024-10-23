import pytest

import weaviate

from ai_journal.storage import create_default_collection


@pytest.fixture(scope="function")
def test_weaviate_client():
    # Instantiate the embedded Weaviate client and pass the OpenAI API key
    # TODO why is this going to the docker version?
    client = weaviate.connect_to_embedded(
        version="1.26.5",
        environment_variables={"ENABLE_MODULES": "text2vec-ollama,generative-ollama"},
    )

    while not client.is_ready():
        continue

    try:
        client.collections.delete_all()
        create_default_collection(client)
        yield client
    finally:
        client.close()
