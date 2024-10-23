import re
from pathlib import Path

import weaviate
import weaviate.classes.config as wvcc
from weaviate.classes.config import Configure


client = weaviate.connect_to_local(host="localhost")

# client.collections.delete_all()

collection = client.collections.create(
    name="WeaviateJournalChunk",
    vectorizer_config=[
        Configure.NamedVectors.text2vec_ollama(
            name="title_vector",
            source_properties=["title"],
            api_endpoint="http://localhost:11434",
            model="llama3:8b",  # The model to use, e.g. "nomic-embed-text"
        )
    ],
    properties=[
        wvcc.Property(name="content", data_type=wvcc.DataType.TEXT),
        wvcc.Property(name="author", data_type=wvcc.DataType.TEXT),
    ],
)


def chunk_list(lst, chunk_size):
    """Break a list into chunks of the specified size."""
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def split_into_sentences(text):
    """Split text into sentences using regular expressions."""
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def read_and_chunk_files(main_folder_path):
    """Recursively read .md files from the folder path and its subfolders, split into sentences, and chunk every 5 sentences."""
    journal_chunks = []
    data_folder_path = Path(main_folder_path).resolve()
    print(data_folder_path)
    for filename in data_folder_path.rglob("*.md"):
        print(filename.name)
        print(f"Reading {filename.name}...")
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            sentences = split_into_sentences(content)
            sentence_chunks = chunk_list(sentences, 5)
            sentence_chunks = [" ".join(chunk) for chunk in sentence_chunks]
            journal_chunks.extend(sentence_chunks)
    return journal_chunks


if __name__ == "__main__":
    data_location = Path("/app/user_data").resolve()

    # Example usage
    journal_chunks = read_and_chunk_files(data_location)

    len(journal_chunks)

    journal_chunks[0]

    journal = client.collections.get("WeaviateJournalChunk")

    for idx, journal_chunk in enumerate(journal_chunks):
        upload = journal.data.insert(properties={"content": journal_chunk})

    print(f"Uploaded {idx} journal chunks.")
