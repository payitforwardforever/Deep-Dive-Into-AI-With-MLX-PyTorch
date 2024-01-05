import os
from datetime import datetime

PREFIX = """
✏️If you want to provide feedback, please submit an issue instead of a pull request. I won't be able to merge your requests. Thank you for your understanding.

Notes on Contributions
----------------------
[CONTRIBUTING.md](../CONTRIBUTING.md)

Notes on Pull Requests and Issues
---------------------------------
[NOTES_ON_PULL_REQUESTS_AND_ISSUES.md](../NOTES_ON_PULL_REQUESTS_AND_ISSUES.md)

# Notes on Sidebars

Unlike other documentation, sidebars in my book are NOT optional. They are core fundamental parts of the book.

Without a solid understanding of the concepts made easy in sidebars, you will not be able to fully understand the rest of the book.

Information in sidebars is presented in a way that is easy to understand and digest. They are not meant to be read in order.

Informational snippets that could be referenced in multiple places in the book are placed in the `book/sidebars` folder.
"""

ITEM_NAME = "Sidebars"
OUTPUT = 'README.md'
EXCLUDE_DIRS = ['images']
ROOT_DIR = '.'

def format_title(filename):
    # Remove the file extension and replace dashes with spaces
    name_without_ext = os.path.splitext(filename)[0].replace('-', ' ')
    # Capitalize the first letter of each word
    return name_without_ext.title()

def generate_markdown_list(dir_path):
    sections = {}
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]  # Exclude specified directories
        section = os.path.relpath(root, dir_path)
        if section == '.':
            continue  # Skip the root directory itself for section listing
        section = section.replace('_', ' ').title()  # Format the section heading
        items = []
        for file in files:
            if not file.startswith('.') and file.endswith('.md'):  # Ignore hidden and non-markdown files
                formatted_title = format_title(file)
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, dir_path)
                item_str = f"- [{formatted_title}]({relative_path})"
                items.append(item_str)
        if items:
            items.sort()  # Sort the items within their section
            sections[section] = items  # Store the sorted items in the dictionary under their section

    markdown_list = []
    for section in sorted(sections.keys()):  # Sort the sections alphabetically before adding to markdown
        section_str = f"## {section}\n"
        markdown_list.append(section_str)
        print('\n', section_str)
        print('\n'.join(sections[section]))
        markdown_list.extend(sections[section])  # Add sorted items
        markdown_list.append('\n')  # Add newline after each section for spacing

    return '\n'.join(markdown_list)  # Join all markdown entries

print(f"Making a list of {ITEM_NAME} in {OUTPUT}...")

with open(OUTPUT, 'w') as f:
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    f.write(PREFIX)
    f.write(f"Auto-generated list of sidebars: {date_time}\n\n")
    f.write(f"# {ITEM_NAME}\n\n")  # Add two newlines for spacing after the title
    markdowns = generate_markdown_list(ROOT_DIR)
    f.write(markdowns)  # Write the markdown content