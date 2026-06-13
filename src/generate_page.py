import os
from pathlib import Path
# FIXED: Changed import path to target the correct file 'markdown_to_html_node.py'
from markdown_to_html_node import markdown_to_html_node

def extract_title(markdown: str) -> str:
    """
    Extracts the single h1 title (# Title) from markdown content.
    Raises a ValueError if no h1 title is found.
    """
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 title found in the markdown content.")

def generate_page(
    from_path: str, 
    template_path: str, 
    dest_path: str | Path, 
    basepath: str
) -> None:
    """
    Generates a full HTML page from a markdown file and a template file.
    Replaces {{ Title }}, {{ Content }}, and updates root paths with basepath.
    Creates necessary destination subdirectories automatically.
    """
    # 1. Print generation tracking message
    print(f" * {from_path} {template_path} -> {dest_path}")

    # 2. Read the markdown file with safety checks
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Source markdown file not found: {from_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # 3. Read the template file with safety checks
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # 4. Convert markdown to HTML string
    # This securely invokes your custom ParentNode wrapper mapping logic
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # 5. Extract the page title
    page_title = extract_title(markdown_content)

    # 6. Replace placeholders and inject basepath prefixing
    full_html = template_content.replace("{{ Title }}", page_title)
    full_html = full_html.replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    # 7. Write the final HTML file to dest_path
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(
    dir_path_content: str, 
    template_path: str, 
    dest_dir_path: str, 
    basepath: str
) -> None:
    """
    Crawls the content directory recursively.
    For each file found, it updates the suffix to .html and generates the page.
    Replicates directory structures down to destination path.
    """
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Content directory not found: {dir_path_content}")

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            # Target files only; safely switches the extension out to .html
            dest_html_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            # Recursively pass subdirectories along down the chain
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
