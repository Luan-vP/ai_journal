import dspy

# TODO unpack these here to uncouple the frontend unpacking from the variable names
create_prompt = dspy.Predict("therapy_topic -> effective_journalling_prompt")

def generate_writing_prompt(therapy_topic: str):
    response = create_prompt(therapy_topic=therapy_topic)
    effective_journalling_prompt = response.effective_journalling_prompt
    return {"message": effective_journalling_prompt}