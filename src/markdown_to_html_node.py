from blocktype import BlockType, block_to_block_type
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from splitnodes import text_to_textnodes
from markdown_blocks import markdown_to_blocks

def extract_title(markdown):
    """
    Extracts the first h1 header from a markdown string.
    Strips the '#' and any surrounding whitespace.
    Raises an Exception if no h1 header is found.
    """
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
        # Edge case: handles '#' directly followed by title text without a space if needed, 
        # but standardized markdown requires a space.
        elif line.strip() == "#":
            continue
            
    raise Exception("Invalid markdown: Missing an h1 header")

def markdown_to_html_node(markdown: str) -> ParentNode:
    # Helper to convert inline markdown text into a list of HTML leaf nodes
    def text_to_children(text: str) -> list[LeafNode]:
        text_nodes = text_to_textnodes(text)
        html_children = []
        for text_node in text_nodes:
            html_children.append(text_node_to_html_node(text_node))
        return html_children

    # 1. Split markdown into broad blocks (assumes markdown_to_blocks is available)
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    # 2. Loop over blocks and generate appropriate ParentNode wrapper trees
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            block_nodes.append(ParentNode(tag="p", children=children))
            
        elif block_type == BlockType.HEADING:
            # Determine heading weight by counting leading hashes
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            # Extract content text following the trailing space
            text = block[level + 1:]
            children = text_to_children(text)
            block_nodes.append(ParentNode(tag=f"h{level}", children=children))
            
        elif block_type == BlockType.CODE:
            # Special manual case: extract inner code content and bypass inline evaluation
            text = block[4:-3].strip("\n")
            code_text_node = TextNode(text, TextType.PLAIN_TEXT)
            code_html_node = text_node_to_html_node(code_text_node)
            
            # Wrap standard code layout syntax: <pre><code>...</code></pre>
            inner_code_wrapper = ParentNode(tag="code", children=[code_html_node])
            block_nodes.append(ParentNode(tag="pre", children=[inner_code_wrapper]))
            
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_line = line[1:]
                if cleaned_line.startswith(" "):
                    cleaned_line = cleaned_line[1:]
                cleaned_lines.append(cleaned_line)
            
            text = "\n".join(cleaned_lines)
            children = text_to_children(text)
            block_nodes.append(ParentNode(tag="blockquote", children=children))
            
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                item_text = line[2:]  # Cuts off "- "
                children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag="li", children=children))
            block_nodes.append(ParentNode(tag="ul", children=li_nodes))
            
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                dot_index = line.find(". ")
                item_text = line[dot_index + 2:]  # Handles variable digit widths (1., 10., etc.)
                children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag="li", children=children))
            block_nodes.append(ParentNode(tag="ol", children=li_nodes))

    # 3. Consolidate list elements under a primary container div wrapper
    return ParentNode(tag="div", children=block_nodes)
