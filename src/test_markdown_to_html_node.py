import unittest
from markdown_to_html_node import markdown_to_html_node, extract_title

# Mocking markdown_to_blocks since it's defined outside this script
# Replace this with your actual import if you have it in a separate file
def markdown_to_blocks(markdown: str) -> list[str]:
    # Simple block splitter for test evaluation isolation
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_markdown_to_html_node_paragraph(self):
        markdown = "This is a plain paragraph with **bold** and *italic* text."
        node = markdown_to_html_node(markdown)
        
        # Verify root structural container
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        
        # Verify inner paragraph structure
        p_node = node.children[0]
        self.assertEqual(p_node.tag, "p")
        
        # Check raw serialization output
        expected_html = "<div><p>This is a plain paragraph with <b>bold</b> and <i>italic</i> text.</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_markdown_to_html_node_headings(self):
        markdown = "# Heading 1\n\n### Heading 3"
        node = markdown_to_html_node(markdown)
        
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "h3")
        
        expected_html = "<div><h1>Heading 1</h1><h3>Heading 3</h3></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_markdown_to_html_node_code_block(self):
        # Testing that raw code blocks don't parse internal markdown delimiters like * or **
        markdown = "```\ndef test_func():\n    # This **should not** be bold\n    return *italic_test*\n```"
        node = markdown_to_html_node(markdown)
        
        # Structure check: div -> pre -> code -> leaf raw value
        pre_node = node.children[0]
        self.assertEqual(pre_node.tag, "pre")
        
        code_node = pre_node.children[0]
        self.assertEqual(code_node.tag, "code")
        
        expected_html = (
            "<div><pre><code>def test_func():\n"
            "    # This **should not** be bold\n"
            "    return *italic_test*</code></pre></div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_markdown_to_html_node_blockquote(self):
        markdown = "> This is a blockquote\n> containing **bold inline text**"
        node = markdown_to_html_node(markdown)
        
        blockquote_node = node.children[0]
        self.assertEqual(blockquote_node.tag, "blockquote")
        
        expected_html = "<div><blockquote>This is a blockquote\ncontaining <b>bold inline text</b></blockquote></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_markdown_to_html_node_lists(self):
        markdown = "- First item with `inline code`\n- Second item"
        node = markdown_to_html_node(markdown)
        
        ul_node = node.children[0]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 2)
        self.assertEqual(ul_node.children[0].tag, "li")
        
        expected_html = "<div><ul><li>First item with <code>inline code</code></li><li>Second item</li></ul></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_markdown_to_html_node_ordered_lists(self):
        # CHANGED: Changed "10." to "3." to comply with sequential step rules
        markdown = "1. Item 1\n2. Item 2\n3. Item 3 with a [link](https://boot.dev)"
        node = markdown_to_html_node(markdown)
        
        ol_node = node.children[0]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 3)
        
        expected_html = (
            "<div><ol><li>Item 1</li><li>Item 2</li>"
            '<li>Item 3 with a <a href="https://boot.dev">link</a></li></ol></div>'
        )
        self.assertEqual(node.to_html(), expected_html)

class TestExtractTitle(unittest.TestCase):
    def test_standard_title(self):
        # Test basic functional requirement
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_title_with_whitespace(self):
        # Test stripping of leading and trailing whitespace
        markdown = "#    Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_multiline_markdown(self):
        # Test extracting h1 when it's mixed with other markdown elements
        markdown = """
        Some introductory text here.
        
        # Actual Title Here
        
        ## Subsection
        - Item 1
        """
        self.assertEqual(extract_title(markdown), "Actual Title Here")

    def test_missing_h1_exception(self):
        # Test that an exception is raised when h1 is completely missing
        markdown = """
        ## This is only an h2
        This text has no level 1 header.
        """
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Invalid markdown: Missing an h1 header")

    def test_false_h1_match(self):
        # Test that multiple '#' signs (like h2, h3) do not trigger a false match
        markdown = "### Not an H1"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
