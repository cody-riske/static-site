import os
from markdown_to_html_node import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    """
    Generates a full HTML page from a markdown file and a template file.
    Replaces {{ Title }} and {{ Content }} placeholders.
    Creates necessary destination subdirectories automatically.
    """
    # 1. Print generation tracking message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 2. Read the markdown file
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Source markdown file not found: {from_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # 3. Read the template file
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # 4. Convert markdown to HTML string
    # Assumes markdown_to_html_node returns an HTMLNode object with a .to_html() method
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # 5. Extract the page title
    page_title = extract_title(markdown_content)

    # 6. Replace the template placeholders
    full_html = template_content.replace("{{ Title }}", page_title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # 7. Write the new full HTML page to dest_path
    # Extract the directory portion of the destination path (e.g., 'public/posts')
    dest_dir = os.path.dirname(dest_path)
    
    # Create missing subdirectories if they do not exist (exist_ok=True prevents errors if it exists)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Crawls the content directory recursively.
    For each .md file found, it generates a corresponding .html file 
    in the destination directory, maintaining the folder structure.
    """
    # Iterate over every item in the current content directory
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(from_path):
            # Only process markdown files
            if from_path.endswith(".md"):
                # Switch out the extension from .md to .html
                # Example: content/blog/tom/index.md -> public/blog/tom/index.html
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_file_name = relative_path.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, dest_file_name)
                
                # Generate this specific page
                generate_page(from_path, template_path, dest_path)
        else:
            # If it's a directory, recursively descend into it
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(from_path, template_path, new_dest_dir)