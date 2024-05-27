from pathlib import Path

user_data_location = Path(__file__).resolve().parent.parent / "user_data"
print(user_data_location)
user_data_location.mkdir(exist_ok=True)


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


def upload_as_embedded_text(text: str):
    embeddings, chunks = embed(text)
    return upload_to_weaviate(embeddings, chunks)

from typing import List

# Split the text into units (words, in this case)
def word_splitter(source_text: str) -> List[str]:
    import re
    source_text = re.sub("\s+", " ", source_text)  # Replace multiple whitespces
    return re.split("\s", source_text)  # Split by single whitespace

def get_chunks_fixed_size_with_overlap(text: str, chunk_size: int, overlap_fraction: float) -> List[str]:
    text_words = word_splitter(text)
    overlap_int = int(chunk_size * overlap_fraction)
    chunks = []
    for i in range(0, len(text_words), chunk_size):
        chunk_words = text_words[max(i - overlap_int, 0): i + chunk_size]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
    return chunks