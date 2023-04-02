from openai_api import setup_openai
from memory_module import setup_memory
from tools import create_summarize_tool, create_refine_tool

# Set up language model
llm = setup_openai()

# Set up memory
memory = setup_memory()

# Define tools
summarize_chain = create_summarize_tool(llm, memory)
refine_chain = create_refine_tool(llm, memory)

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

