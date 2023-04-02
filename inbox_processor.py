from memory_module import ConversationBufferMemory

def process_inbox_item(item, summarize_chain, refine_chain, memory: ConversationBufferMemory):
    memory.chat_memory.add_user_message("""You are a large language model trained by OpenAI. You are designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, you are able to generate human-like text based on the input you receive, allowing you to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

You are constantly learning and improving, and your capabilities are constantly evolving. You are able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, you are able to generate your own text based on the input you receive, allowing you to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, you are a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether someone needs help with a specific question or just wants to have a conversation about a particular topic, you are here to assist.""")

    memory.chat_memory.add_user_message(f"Here is an item from my inbox: {item}. I would like for you to fully understand my reason for writing this inbox item down so you can help me rewrite it concisely and clearly.")

    # Check for understanding
    summary = summarize_chain.predict(human_input="Please concisely and clearly summarize your current understanding of this inbox item.")
    print(f"Summary: {summary}")

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

    isCorrect = input("Correct? (Y/n)")
    while (isCorrect.lower() == "n"):
        corrections = input("Corrections: ")
        memory.chat_memory.add_user_message(corrections)
        final_summary = summarize_chain.predict(human_input="Your understanding was correct but your final note was wrong. Please re-write it concisely and clearly, as if it were written by the user as a 'note to self'. Please take the user's corrections into account")
        print(f"Final Summary: {final_summary}")

        isCorrect = input("Correct? (Y/n)")

    memory.chat_memory.clear()

    return final_summary

