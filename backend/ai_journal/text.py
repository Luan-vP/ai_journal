import re
from pathlib import Path


def chunk_list(lst, chunk_size):
    """Break a list into chunks of the specified size."""
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def split_into_sentences(text):
    """Split text into sentences using regular expressions."""
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def read_and_chunk_files(main_folder_path):
    """Read .md files from the folder path, split into sentences, and chunk every 5 sentences."""
    journal_chunks = []
    data_folder_path = Path(main_folder_path).resolve()
    print(data_folder_path)
    for filename in data_folder_path.iterdir():
        print(filename.name)
        if ".md" in filename.name:
            print(f"Reading {filename.name}...")
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
                sentences = split_into_sentences(content)
                sentence_chunks = chunk_list(sentences, 5)
                sentence_chunks = [" ".join(chunk) for chunk in sentence_chunks]
                journal_chunks.extend(sentence_chunks)
    return journal_chunks
