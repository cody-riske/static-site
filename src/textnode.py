from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN_TEXT = "text (plain)"
    BOLD_TEXT = "**Bold text**"
    ITALIC_TEXT = "_Italic text_"
    CODE_TEXT = "`Code text`"
    LINKS_TEXT = "[anchor text](url)"
    IMAGES_TEXT = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url)
    
    def __repr__(self): 
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINKS_TEXT:
            if not text_node.url:
                raise ValueError("Link TextNode must have a URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGES_TEXT:
            if not text_node.url:
                raise ValueError("Image TextNode must have a URL")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid TextType: {text_node.text_type}")