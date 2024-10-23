import contextlib
import os
import uuid
from pathlib import Path

import weaviate
from weaviate import WeaviateClient
import weaviate.classes.config as wvcc
from weaviate.classes.config import Configure

WEAVIATE_COLLECTION_NAME = (
    os.getenv("WEAVIATE_COLLECTION_NAME") or "WeaviateJournalChunks"
)
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST") or "localhost"

user_data_location = Path(__file__).resolve().parents[2] / "local_data"
print(user_data_location)
user_data_location.mkdir(exist_ok=True)

example_data_location = Path(__file__).resolve().parent.parent / "data"


def read_user_data() -> dict:
    user_data = {}
    for user_data_file in user_data_location.iterdir():
        print(user_data_file.stem)
        with open(user_data_file, "r") as file:
            user_data[user_data_file.stem] = file.read()
    return user_data


def write_to_new_file(content: str):
    # new timestamp for the file name
    import datetime

    new_file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".md"

    new_file_path = user_data_location / new_file_name
    with open(new_file_path, "w") as file:
        file.write(content)
    return new_file_name


@contextlib.contextmanager
def get_weaviate_client():
    client = weaviate.connect_to_local(host=WEAVIATE_HOST)

    try:
        yield client
    finally:
        client.close()


def create_default_collection(weaviate_client: WeaviateClient):
    weaviate_client.collections.create(
        name=WEAVIATE_COLLECTION_NAME,
        vectorizer_config=[
            Configure.NamedVectors.text2vec_ollama(
                name="title_vector",
                source_properties=["title"],
                api_endpoint="http://localhost:11434",  # TODO switch this to docker with a startup scripts
                model="llama3:8b",
            )
        ],
        generative_config=Configure.Generative.ollama(
            api_endpoint="http://localhost:11434"
        ),
        properties=[
            wvcc.Property(name="content", data_type=wvcc.DataType.TEXT),
            wvcc.Property(name="author", data_type=wvcc.DataType.TEXT),
        ],
    )


def upload_text_to_weaviate_collection(
    text: str, weaviate_client: weaviate.WeaviateClient
) -> uuid.UUID:
    collection = weaviate_client.collections.get(WEAVIATE_COLLECTION_NAME)

    uuid = collection.data.insert({"text": text})

    return uuid
