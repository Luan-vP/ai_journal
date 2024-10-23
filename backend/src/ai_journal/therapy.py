import logging

import dspy
import dspy.retrieve
from dspy.retrieve.weaviate_rm import WeaviateRM

from .storage import get_weaviate_client, WEAVIATE_COLLECTION_NAME
from .lm import lm

logger = logging.getLogger(__name__)

dspy.configure(lm=lm)

# TODO unpack these here to uncouple the frontend unpacking from the variable names
create_prompt = dspy.Predict("therapy_topic -> effective_journalling_prompt")

def generate_writing_prompt(therapy_topic: str):
    response = create_prompt(therapy_topic=therapy_topic)
    effective_journalling_prompt = response.effective_journalling_prompt
    return {"message": effective_journalling_prompt}

generate_post_writing_analysis = dspy.Predict("journal_entry -> therapeutic_observation")

def generate_post_writing_analysis(journal_entry: str, journal_prompt: str = "" ):
    create_therapists_observations = dspy.Predict("journal_entry, journal_prompt, past_journal_entries -> therapists_observations")
    
    past_journal_entries = retrieve_from_weaviate(f"{journal_prompt} {journal_entry}")
    response = create_therapists_observations(
        journal_prompt=journal_prompt,
        journal_entry=journal_entry,
        past_journal_entries=past_journal_entries)
    therapists_observations = response.therapists_observations
    return{"message": therapists_observations}

def retrieve_from_weaviate():

    with get_weaviate_client() as weaviate_client:

        retriever_model = dspy.WeaviateRM(
            weaviate_collection_name=WEAVIATE_COLLECTION_NAME,
            weaviate_client=weaviate_client 
        )

        results = retriever_model("Explore the significance of quantum computing", k=2)
        concat_results = "|".join([result.long_text for result in results])
        
        logger.debug(f"{concat_results =}")
        return concat_results
    
class JournalAnalyzer(dspy.Module):
    def __init__(self, k, weaviate_client):
        self.k =  k  # The number of past journal entries to retrieve
        self.weaviate_client = weaviate_client
        
        self.retriever_model = WeaviateRM(
            weaviate_collection_name=WEAVIATE_COLLECTION_NAME,
            weaviate_client=self.weaviate_client 
        )
        self.therapist = dspy.Predict(
            "journal_entry, past_relevant_journal_entries -> therapeutic_analysis"
        )

    def forward(self, journal_entry):
        past_relevant_journal_entries = self.retriever_model(journal_entry, self.k)
        analysis = self.therapist(
            journal_entry=journal_entry,
            past_relevant_journal_entries="\n".join(past_relevant_journal_entries)
        )
        print(analysis)

        return analysis.therapeutic_analysis

    
    def __del__(self):
        self.weaviate_client.close()
