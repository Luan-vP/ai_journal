import dspy
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


create_post_analysis = dspy.Predict("journal_entry -> therapeutic_insight")


class JournalEntry(BaseModel):
    journal_entry: str


@app.post("/post_analysis")
def get_post_analysis(entry: JournalEntry):
    response = create_post_analysis(journal_entry=entry.journal_entry)
    therapeutic_insight = response.therapeutic_insight
    return {"message": therapeutic_insight}
