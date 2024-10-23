import dspy

lm = dspy.OllamaLocal(model="llama3")

dspy.configure(lm=lm)
