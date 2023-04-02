import re

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    return content

def parse_input_file(content):
    items = []
    item = ""
    prev_indent = 0

    for line in content:
        match = re.match(r"(\s*)[-*+>0-9.]+(\s+)(.+)", line)
        if match:
            indent = len(match.group(1))
            item_text = match.group(3).strip()

            if indent > prev_indent:
                item += " " + item_text
            else:
                if item:
                    items.append(item)
                item = item_text

            prev_indent = indent
        else:
            if item:
                items.append(item)
                item = ""

    if item:
        items.append(item)

    return items

