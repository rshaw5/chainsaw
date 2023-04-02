from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory

# Set up language model
llm = OpenAI(temperature=0.8)

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history")

# Define summarize tool
summarize_template = """You are a chatbot having a conversation with a human. {chat_history} Human: {human_input} Chatbot:"""
summarize_variables = ["chat_history", "human_input"]
summarize_prompt = PromptTemplate(template=summarize_template, input_variables=summarize_variables)
summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt, verbose=True, memory=memory)

# Define refine tool
refine_template = """Here is an item from my inbox: {input}. I would like for you to fully understand my reason for writing this inbox item down. Please ask me clarifying questions (if you have any) until you are confident you understand this inbox item. If you have no questions, please say so."""
refine_variables = ["input"]
refine_prompt = PromptTemplate(template=refine_template, input_variables=refine_variables)
refine_chain = LLMChain(llm=llm, prompt=refine_prompt, verbose=True, memory=memory)


# Get the inbox item
item = input("Item: ")
memory.chat_memory.add_user_message(f"Here is an item from my inbox: {item}. I would like for you to fully understand my reason for writing this inbox item down so you can help me rewrite it concisely and clearly.")

# Check for understanding
summary = summarize_chain.predict(human_input="Please concisely and clearly summarize your current understanding of this inbox item.")
print(f"Summary: {summary}")

isCorrect = "y"
isCorrect = input("Correct? (Y/n)")

# If necessary, ask clarifying questions
while (isCorrect.lower() == "n"):
    # Formulate questions
    questions = refine_chain.run(input=item)
    print(questions)
    memory.chat_memory.add_ai_message(questions)
    
    # Receive answers
    answers = input("Answers: ")
    memory.chat_memory.add_user_message(answers)

    # Check for understanding
    summary = summarize_chain.predict(human_input="Please concisely and clearly summarize your current understanding of this inbox item.")
    print(f"Summary: {summary}")

    isCorrect = input("Correct? (Y/n)")

final_summary = summarize_chain.predict(human_input="You now have the correct understanding. Please summarize this item concisely and clearly, as if it was written by the user as a 'note to self'.")
print(f"Final Summary: {final_summary}")
