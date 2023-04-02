from langchain import LLMChain, PromptTemplate

def create_summarize_tool(llm, memory, verbose=False):
    summarize_template = """You are a chatbot having a conversation with a human. {chat_history} Human: {human_input} Chatbot:"""
    summarize_variables = ["chat_history", "human_input"]
    summarize_prompt = PromptTemplate(template=summarize_template, input_variables=summarize_variables)
    return LLMChain(llm=llm, prompt=summarize_prompt, verbose=verbose, memory=memory)

def create_refine_tool(llm, memory, verbose=False):
    refine_template = """Here is an item from my inbox: {input}. I would like for you to fully understand my reason for writing this inbox item down. Please ask me clarifying questions (if you have any) until you are confident you understand this inbox item. If you have no questions, please say so."""
    refine_variables = ["input"]
    refine_prompt = PromptTemplate(template=refine_template, input_variables=refine_variables)
    return LLMChain(llm=llm, prompt=refine_prompt, verbose=verbose, memory=memory)

