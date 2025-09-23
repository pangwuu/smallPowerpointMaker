
from pathlib import Path
import urllib.parse

def generate_file_list():
    root = Path("Complete slides")
    files = sorted(root.glob("**/*.pptx"), reverse=True)
    html_list = []
    for file in files:
        # URL encode the file path to handle spaces and other special characters
        encoded_path = urllib.parse.quote(str(file))
        html_list.append(f'<li><a href="{encoded_path}">{file.name}</a></li>')
    return "\n".join(html_list)

def main():
    file_list_html = generate_file_list()
    with open("index.html", "r") as f:
        content = f.read()
    
    content = content.replace("<!-- File list will be generated here -->", file_list_html)

    with open("index.html", "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()

