import dspy
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# TODO very danger
from ai_journal import storage

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


turbo = dspy.OpenAI("gpt-3.5-turbo")
dspy.settings.configure(lm=turbo)


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


@app.get("/dump")
def dump():
    return {"message": storage.read_user_data()}
