```mermaid
flowchart TD
    A["Hi! What would you like to write about?"]--> B{{"Retrieval"}}
    B --> C{{"Insight"}}
    C --> F{{"Display"}}
    C ---> D["Write"]
    D --> E{{"Submit + Upload"}}
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
