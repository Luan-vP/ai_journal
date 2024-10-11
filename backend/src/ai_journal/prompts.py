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


class GenerateWritingPrompt(dspy.Signature):
    """topic, context -> writing_prompt"""

    writing_topic = dspy.InputField(
        prompt="The subject the client would like to explore in their journal."
    )
    context = dspy.InputField(
        prompt="The client's previous journal entries and the conversation so far."
    )
    writing_prompt = dspy.OutputField(
        prompt="A writing prompt that will help the client explore their emotions in depth."
    )


class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_writing_prompt = dspy.ChainOfThought(GenerateWritingPrompt)

    def forward(self, writing_topic):
        context = self.retrieve(writing_topic).passages
        writing_prompt = self.generate_writing_prompt(
            context=context, writing_topic=writing_topic
        )
        # TODO change this output signature
        return dspy.Prediction(context=context, answer=writing_prompt.answer)
