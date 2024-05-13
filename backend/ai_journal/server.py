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

USE_OLLAMA = os.getenv("USE_OLLAMA", False)

if USE_OLLAMA in ["True", "true", "1"]:
    lm = dspy.OllamaLocal(model="llama3", base_url="http://host.docker.internal:11434")
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


create_post_analysis = dspy.Predict(
    "journal_entry -> one_point_to_observe_over_the_next_week"
)


class JournalEntry(BaseModel):
    journal_entry: str


@app.post("/post_analysis")
def get_post_analysis(entry: JournalEntry):
    response = create_post_analysis(journal_entry=entry.journal_entry)
    one_point_to_observe_over_the_next_week = (
        response.one_point_to_observe_over_the_next_week
    )
    filename = storage.write_to_new_file(
        entry.journal_entry + "Insight:" + one_point_to_observe_over_the_next_week
    )
    print(f"New entry written to {filename}")
    return {"message": one_point_to_observe_over_the_next_week}


@app.post("/save")
def save_entry_to_file(entry: JournalEntry):
    filename = storage.write_to_new_file(entry.journal_entry)
    logger.debug(f"New entry written to {filename}")


class UserData(BaseModel):
    data: dict[str, str]


# TODO very danger
@app.get("/dump", response_model=UserData)
def dump():
    return {"data": storage.read_user_data()}
