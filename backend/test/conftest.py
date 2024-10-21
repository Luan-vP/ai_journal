import pytest

import weaviate
import weaviate.classes.config as wvcc
from weaviate.classes.config import Configure

from ai_journal.storage import WEAVIATE_COLLECTION_NAME

@pytest.fixture(scope="module")
def test_weaviate_client():
    # Instantiate the embedded Weaviate client and pass the OpenAI API key
    # TODO why is this going to the docker version?
    client = weaviate.connect_to_embedded(
        version="1.26.5",
        environment_variables={"ENABLE_MODULES":"text2vec-ollama,generative-ollama"}
        )

    while not client.is_ready():
        continue 

    try:
        client.collections.delete_all()
        client.collections.create(
        name=WEAVIATE_COLLECTION_NAME,
        vectorizer_config=[
            Configure.NamedVectors.text2vec_ollama(
                name="title_vector",
                source_properties=["title"],
                api_endpoint="http://localhost:11434", # TODO switch this to docker with a startup scripts
                model="llama3:8b",
            )
        ],
        generative_config=Configure.Generative.ollama(
            api_endpoint="http://host.docker.internal:11434"
        ),
        properties=[
            wvcc.Property(name="content", data_type=wvcc.DataType.TEXT),
            wvcc.Property(name="author", data_type=wvcc.DataType.TEXT),
        ],
        )
        yield client
    finally:
        client.close()