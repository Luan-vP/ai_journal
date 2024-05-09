```mermaid
flowchart TD
    A["Hi! What would you like to write about?"]--> B{{"Retrieval"}}
    B --> C{{"Insight"}}
    C --> F{{"Display"}}
    C ---> D["Write"]
    D --> E{{"Submit + Upload"}}
```

Todos:
- [ ] Add a timer
- [ ] Add EmotionWheel UI selector
- [ ] Mac Application Wrapper
- [ ] Update UI styling 
- [ ] Impliment RAG for insights