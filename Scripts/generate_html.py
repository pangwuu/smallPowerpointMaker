
from pathlib import Path
import urllib.parse
import re

def generate_file_list():
    root = Path("Complete slides")
    files = sorted(root.glob("**/*.pptx"), reverse=True)
    html_list = []
    for file in files:
        encoded_path = urllib.parse.quote(str(file))
        # Add a class to the anchor tag
        html_list.append(f'<li><a class="download-link" href="{encoded_path}">{file.name}</a></li>')
    html_list.sort()
    return "\n".join(html_list)

def main():
    file_list_html = generate_file_list()
    with open("index.html", "r") as f:
        content = f.read()

    start_marker = "<!-- START_FILE_LIST -->"
    end_marker = "<!-- END_FILE_LIST -->"
    
    # The new content to be injected, including the markers
    new_block = f"{start_marker}\n{file_list_html}\n        {end_marker}"
    
    # The regex to find the block to replace
    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
    
    content = pattern.sub(new_block, content)

    with open("index.html", "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()

