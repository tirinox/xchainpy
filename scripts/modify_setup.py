"""
This script is used to update the setup.py file with the load_description function.
The load_description function load package description from README.md file.

The fast is that swagger_codegen spoils setup.py file by removing the long_description field.
This script adds the long_description field back to the setup.py file. Also, it modifies the setup call arguments.

Example usage:

python misc/example_setup.py -o misc/mod_setup.py

"""
import sys
import re


def insert_load_description(content):
    if "def load_description():" in content:
        print("load_description is already defined. Skipping")
        return content

    # find "setup(" location
    setup_call_match = re.search(r'setup\s*\(', content)
    if setup_call_match:
        insertion_index = setup_call_match.start()

        with open("misc/load_description.py") as f:
            code = f.read().strip()
            code = f'\n{code}\n\n'

        content = content[:insertion_index] + code + content[insertion_index:]
    else:
        print("WARNING: No setup() call found. New function was not inserted.")

    return content


def find_matching_paren(text, start_index):
    """
    Given a string and the index of an opening parenthesis,
    return the index of the corresponding closing parenthesis.
    """
    count = 0
    for i in range(start_index, len(text)):
        if text[i] == '(':
            count += 1
        elif text[i] == ')':
            count -= 1
            if count == 0:
                return i
    return -1


def modify_setup_call_arguments(content):

    # --- 2. Locate the complete setup() call ---
    setup_start = content.find("setup(")
    if setup_start == -1:
        print("ERROR: No setup() call found in the file.")
        return

    opening_paren_index = content.find("(", setup_start)
    if opening_paren_index == -1:
        print("ERROR: Malformed setup() call: no opening parenthesis found.")
        return

    matching_paren_index = find_matching_paren(content, opening_paren_index)
    if matching_paren_index == -1:
        print("ERROR: Could not find matching closing parenthesis for setup() call.")
        return

    # Extract the complete original setup() call.
    original_setup_call = content[setup_start:matching_paren_index+1]

    # --- 3. Process the parameters inside setup() ---
    # Extract the content inside the parentheses.
    setup_params = content[opening_paren_index+1: matching_paren_index]

    # Remove any existing long_description and long_description_content_type entries.
    setup_params = re.sub(
        r'long_description\s*=\s*(?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|".*?"|\'.*?\')\s*,?\n?',
        '',
        setup_params
    )
    setup_params = re.sub(
        r'long_description_content_type\s*=\s*(?:"text/markdown"|\'text/markdown\')\s*,?\n?',
        '',
        setup_params
    )

    # Clean up trailing whitespace and ensure there's a comma before appending new args.
    setup_params = setup_params.rstrip()
    if setup_params and not setup_params.endswith(','):
        setup_params += ','

    new_args = (
        '\n    long_description=load_description(),\n'
        '    long_description_content_type="text/markdown",\n'
    )
    setup_params += new_args

    # --- 4. Build the updated setup() call ---
    updated_setup_call = "setup(\n" + setup_params + ")"

    # Replace the original setup() call with the updated one.
    updated_content = content[:setup_start] + updated_setup_call + content[matching_paren_index+1:]

    return updated_content


def update_setup_py(file_path, output_path=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    output_path = output_path or file_path

    content = insert_load_description(content)
    content = modify_setup_call_arguments(content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    # Usage: python modify_setup.py <file_path> -o <output_path>
    file_path = sys.argv[1]
    output_path = None
    if len(sys.argv) > 3 and sys.argv[2] == "-o":
        output_path = sys.argv[3]

    update_setup_py(file_path, output_path)
