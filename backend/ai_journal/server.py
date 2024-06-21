import os
from logging import DEBUG, Logger

import dspy
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# TODO very danger
from ai_journal import storage

logger = Logger(__file__, DEBUG)

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Setup weaviate host for docker
os.environ["WEAVIATE_HOST"] = "weaviate"
from rag_router.router import router

# Adds the /generative_search endpoint
app.include_router(router)

USE_OLLAMA = os.getenv("USE_OLLAMA", False)

if USE_OLLAMA in ["True", "true", "1"]:
    lm = dspy.OllamaLocal(
        model="llama3", base_url="http://host.docker.internal:11434"
    )
else:
    lm = dspy.OpenAI("gpt-3.5-turbo")
dspy.settings.configure(lm=lm)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# TODO unpack these here to uncouple the frontend unpacking from the variable names
create_prompt = dspy.Predict("therapy_topic -> effective_journalling_prompt")


@app.get("/writing_prompt")
def get_writing_prompt(therapy_topic: str):
    response = create_prompt(therapy_topic=therapy_topic)
    effective_journalling_prompt = response.effective_journalling_prompt
    return {"message": effective_journalling_prompt}


create_post_analysis = dspy.Predict("journal_entry -> therapeutic_observation")


class Input(BaseModel):
    text_input: str


@app.post("/post_analysis")
def get_post_analysis(input: Input):
    response = create_post_analysis(journal_entry=input.text_input)
    therapeutic_observation = response.therapeutic_observation
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
def dump():
    return {"data": storage.read_user_data()}
