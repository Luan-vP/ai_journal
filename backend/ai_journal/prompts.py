import dspy

turbo = dspy.OpenAI("gpt-3.5-turbo")
dspy.settings.configure(lm=turbo)

# The flow is as follows:
# Recieve an insight from the frontend
# Suggest a helpful writing prompt to journal on
# Time a 20 minute writing session
# Analyse and reflect on the writing

system_prompt = """
    You are a psychotherapist who is helping a client explore their emotions through journalling."""


class WritingPrompt(dspy.Signature):
    "topic, context -> writing_prompt"
    topic = dspy.InputField(
        "The subject the client would like to explore in their journal."
    )
    context = dspy.InputField(
        "The client's previous journal entries and the conversation so far."
    )
    writing_prompt = dspy.OutputField(
        "A writing prompt that will help the client explore their emotions in depth."
    )
