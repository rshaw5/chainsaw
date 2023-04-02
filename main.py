import argparse
from openai_api import setup_openai
from memory_module import setup_memory
from tools import create_summarize_tool, create_refine_tool
from file_manager import read_input_file, parse_input_file
from inbox_processor import process_inbox_item

def process_single_item(summarize_chain, refine_chain, memory):
    item = input("Item: ")
    final_summary = process_inbox_item(item, summarize_chain, refine_chain, memory)
    return final_summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Path to the text or markdown file.", nargs='?', default=None)
    args = parser.parse_args()

    file_path = args.file_path

    # Set up language model
    llm = setup_openai()

    # Set up memory
    memory = setup_memory()

    # Define tools
    summarize_chain = create_summarize_tool(llm, memory)
    refine_chain = create_refine_tool(llm, memory)

    if file_path is not None:
        content = read_input_file(file_path)
        inbox_items = parse_input_file(content)

        with open('inbox-clarified.md', 'a') as output_file:
            for item in inbox_items:
                final_summary = process_inbox_item(item, summarize_chain, refine_chain, memory)
                stripped_summary = final_summary.strip()
                output_file.write(f"- {stripped_summary}\n")

    else:
        while True:
            final_summary = process_single_item(summarize_chain, refine_chain, memory)
            stripped_summary = final_summary.strip()

            with open('inbox-clarified.md', 'a') as output_file:
                output_file.write(f"- {stripped_summary}\n")

            continue_processing = input("Process another item? (Y/n): ")
            if continue_processing.lower() == 'n':
                break

