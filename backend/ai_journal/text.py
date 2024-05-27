from langchain_community.embeddings import OllamaEmbeddings
ollama_emb = OllamaEmbeddings(
    model="llama3:8b",
)

DEFAULT_CHUNK_SIZE=15

# Split the text into units (words, in this case)
def word_splitter(source_text: str) -> list[str]:
    import re
    source_text = re.sub("\s+", " ", source_text)  # Replace multiple whitespces
    return re.split("\s", source_text)  # Split by single whitespace

def get_chunks_fixed_size_with_overlap(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap_fraction: float = 0.0) -> list[str]:
    text_words = word_splitter(text)
    overlap_int = int(chunk_size * overlap_fraction)
    chunks = []
    for i in range(0, len(text_words), chunk_size):
        chunk_words = text_words[max(i - overlap_int, 0): i + chunk_size]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
    return chunks

def embed_text(text: str):
    chunks = get_chunks_fixed_size_with_overlap(text)
    embeddings = ollama_emb.embed_documents(chunks)
    return embeddings