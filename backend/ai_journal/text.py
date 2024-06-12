from langchain_community.embeddings import OllamaEmbeddings

ollama_emb = OllamaEmbeddings(
    model="llama3:8b",
)

DEFAULT_CHUNK_SIZE = 15


# Split the text into units (words, in this case)
def word_splitter(source_text: str) -> list[str]:
    import re

    source_text = re.sub("\s+", " ", source_text)  # Replace multiple whitespces
    return re.split("\s", source_text)  # Split by single whitespace


def get_chunks_fixed_size_with_overlap(
    text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap_fraction: float = 0.0
) -> list[str]:
    text_words = word_splitter(text)
    overlap_int = int(chunk_size * overlap_fraction)
    chunks = []
    for i in range(0, len(text_words), chunk_size):
        chunk_words = text_words[max(i - overlap_int, 0) : i + chunk_size]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
    return chunks


def embed_text_as_chunks(text: str):
    chunks = get_chunks_fixed_size_with_overlap(text)
    embeddings = ollama_emb.embed_documents(chunks)
    return zip(chunks, embeddings)


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
