import os
from logging import DEBUG, Logger

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_router.router import router

# TODO very danger
from ai_journal import storage, therapy

logger = Logger(__file__, DEBUG)

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Adds the /generative_search endpoint
app.include_router(router)

# Setup weaviate host for docker
os.environ["WEAVIATE_HOST"] = "weaviate"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/writing_prompt")
def get_writing_prompt(therapy_topic: str):
    return {"data": therapy.generate_writing_prompt(therapy_topic)}


class Input(BaseModel):
    text_input: str


@app.post("/post_writing_analysis")
def get_post_writing_analysis(input: Input):
    therapeutic_observation = therapy.generate_post_writing_analysis(input.text_input)
    filename = storage.write_to_new_file(
        input.text_input + "Insight:" + therapeutic_observation
    )
    print(f"New entry written to {filename}")
    return {"message": therapeutic_observation}


@app.post("/save")
def save_entry_to_file(input: Input):
    filename = storage.write_to_new_file(input.text_input)
    logger.debug(f"New entry written to {filename}")


class UserData(BaseModel):
    data: dict[str, str]


# TODO very danger
@app.get("/dump", response_model=UserData)
def get_dump():
    return {"data": storage.read_user_data()}
