# AI Journal
An LLM powered journal to help you better understand your thoughts, and improve them over time.


```mermaid
flowchart TD
    A(["Journalling prompt"])
    subgraph journalling_step [ ]
        B[/"User writes an entry"/]
        B --> |1|C["Collect relevant past entries"]
        C --> |2|D{"Ask a clarifying question? (continue loop)"}
        D --> |Yes|E[LLM generated clarifying question]
        E --> |4|B
    end
    D --> |No|EE(["LLM generated insight"])

    A --> B
    DB[("Database")]
    DB --> |retrieve entries|C
    B --> |save entry|DB
```

## Architecture

### Backend

FastAPI server
Ollama + llama3:7b + dspy for LLM pipelines

#### Data

Weaviate
usage +500B/user/day = +182kb / user / year (without embeddings)

### Frontend

Svelte
