from memory_module import ConversationBufferMemory

def process_inbox_item(item, summarize_chain, refine_chain, memory: ConversationBufferMemory):
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

