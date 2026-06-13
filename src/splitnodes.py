import re
from enum import Enum
from textnode import TextNode, TextType

def text_to_textnodes(text: str) -> list[TextNode]:
    # Start with a single plain text node containing everything
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    
    # 1. Split out images and links first (avoids delimiter collision)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # 2. Split bold (Handles both ** and __)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD_TEXT) # <-- ADD THIS LINE
    
    # 3. Split italic (Handles both * and _)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT) # <-- ADD THIS LINE
    
    # 4. Split inline code snippets
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    
    return nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        # UPDATED: Changed TextType.TEXT to TextType.PLAIN_TEXT
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
            
        original_text = node.text
        parts = original_text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: matching delimiter '{delimiter}' not found.")
            
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
                
    return new_nodes

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
            
        remaining_text = node.text
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            sections = remaining_text.split(image_markdown, 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.IMAGES_TEXT, url))
            remaining_text = sections[1]
            
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN_TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
            
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
            
        remaining_text = node.text
        for anchor_text, url in links:
            link_markdown = f"[{anchor_text}]({url})"
            sections = remaining_text.split(link_markdown, 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
                
            new_nodes.append(TextNode(anchor_text, TextType.LINKS_TEXT, url))
            remaining_text = sections[1]
            
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN_TEXT))
            
    return new_nodes

