import pytest


import ai_journal.therapy as therapy


@pytest.mark.parametrize(
    "therapy_topic, journal_entry",
    [
        ("anger", "This is a test journal entry about anger."),
        ("stress", "This is a test journal entry about stress."),
        ("happiness", "This is a test journal entry about happiness."),
        ("sadness", "This is a test journal entry about sadness."),
        ("anxiety", "This is a test journal entry about anxiety."),
    ],
)
def test_generate_post_writing_analysis(
    therapy_topic, journal_entry, test_weaviate_client
):
    # I want to assert that the advice contained information from both
    # the current journal entry, and the retrieved relevant journal entries.

    # I could make sure that the arguments to generative_search contained
    # key document entries, and not others, but that would more be checking
    # weaviates vector search.

    # Instead, I want to make sure that this function is receiving the journal entry,
    # passing it to the dspy pipeline.

    journal_analyzer = therapy.JournalAnalyzer(
        k=3, weaviate_client=test_weaviate_client
    )

    analysis = journal_analyzer(journal_entry)
    assert therapy_topic in analysis
