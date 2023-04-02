from langchain import OpenAI

def setup_openai(temperature=0.8):
    return OpenAI(temperature=temperature)

