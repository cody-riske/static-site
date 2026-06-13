import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes_all_types(self):
        text = "This is **bold** text with an *italic* word and a `code block` and an ![image](https://imgur.com) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" text with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGES_TEXT, "https://imgur.com"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINKS_TEXT, "https://boot.dev")
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_plain_only(self):
        text = "This is just ordinary plain text with no markdown formatting."
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just ordinary plain text with no markdown formatting.", TextType.PLAIN_TEXT)]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_bold_and_italic(self):
        text = "This has **bold** and *italic* back to back."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" back to back.", TextType.PLAIN_TEXT)
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_link_and_image(self):
        text = "An ![image](img.png) followed by a [link](url.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("An ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGES_TEXT, "img.png"),
            TextNode(" followed by a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINKS_TEXT, "url.com")
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        # Depending on your implementation of splits, an empty string should 
        # either return an empty list or a single plain text node with "" text.
        # This checks for a clean return without crashing.
        self.assertIsInstance(nodes, list)

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        node = TextNode("Hello **world** clear text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("Hello ", TextType.PLAIN_TEXT),
            TextNode("world", TextType.BOLD_TEXT),
            TextNode(" clear text", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_at_start(self):
        node = TextNode("`code` at the start", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected = [
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" at the start", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_multiple_delimiters(self):
        node = TextNode("Start **bold1** middle **bold2** end", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("Start ", TextType.PLAIN_TEXT),
            TextNode("bold1", TextType.BOLD_TEXT),
            TextNode(" middle ", TextType.PLAIN_TEXT),
            TextNode("bold2", TextType.BOLD_TEXT),
            TextNode(" end", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_ignore_non_plain_text(self):
        nodes = [
            TextNode("Bypassed bold node", TextType.BOLD_TEXT),
            TextNode("Plain `code` node", TextType.PLAIN_TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        expected = [
            TextNode("Bypassed bold node", TextType.BOLD_TEXT),
            TextNode("Plain ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" node", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_missing_closing_delimiter_raises_error(self):
        node = TextNode("This markdown has an **unclosed bold tag", TextType.PLAIN_TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertIn("matching delimiter", str(context.exception))

class TestMarkdownExtractions(unittest.TestCase):

    def test_extract_markdown_images(self):
        """Test extraction of a single image and multiple images."""
        # FIXED: Removed the backslashes before the opening brackets
        text = "This is text with an ![image](https://imgur.com) and another ![second image](https://imgur.com)"
        expected = [
            ("image", "https://imgur.com"),
            ("second image", "https://imgur.com")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_ignores_links(self):
        """Test that image extraction ignores standard markdown links."""
        # FIXED: Removed the backslash before the opening bracket
        text = "This is a link [Google](https://google.com) but this is an image ![logo](https://logo.com)"
        expected = [("logo", "https://logo.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        """Test extraction of standard markdown links."""
        text = "Click [here](https://boot.dev) to learn coding or [here](https://google.com) to search."
        expected = [
            ("here", "https://boot.dev"),
            ("here", "https://google.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_ignores_images(self):
        """Test that link extraction ignores markdown images (no ! allowed)."""
        # FIXED: Removed the backslash before the opening bracket
        text = "This is an ![image](https://image.com) and this is a [link](https://link.com)"
        expected = [("link", "https://link.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extraction_with_no_matches(self):
        """Test that both functions return an empty list if no syntax matches."""
        text = "This text has plain words, **bold text**, and `code` but no images or links."
        self.assertEqual(extract_markdown_links(text), [])
        self.assertEqual(extract_markdown_images(text), [])

class TestInlineMarkdownSplitting(unittest.TestCase):
    
    # --- Tests for split_nodes_image ---
    
    def test_split_image_single(self):
        node = TextNode("This is an image ![logo](https://example.com) in text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is an image ", TextType.PLAIN_TEXT),
            TextNode("logo", TextType.IMAGES_TEXT, "https://example.com"),
            TextNode(" in text", TextType.PLAIN_TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_multiple(self):
        node = TextNode("![one](1.png) text ![two](2.png)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("one", TextType.IMAGES_TEXT, "1.png"),
            TextNode(" text ", TextType.PLAIN_TEXT),
            TextNode("two", TextType.IMAGES_TEXT, "2.png")
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_no_images(self):
        node = TextNode("This text has no images at all.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_image_ignores_non_plain_text(self):
        node = TextNode("![ignore](me.png)", TextType.LINKS_TEXT, "https://link.com")
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])


    # --- Tests for split_nodes_link ---

    def test_split_link_single(self):
        node = TextNode("Click [here](https://boot.dev) to learn.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Click ", TextType.PLAIN_TEXT),
            TextNode("here", TextType.LINKS_TEXT, "https://boot.dev"),
            TextNode(" to learn.", TextType.PLAIN_TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_multiple(self):
        node = TextNode("[first](url1) mid [second](url2)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINKS_TEXT, "url1"),
            TextNode(" mid ", TextType.PLAIN_TEXT),
            TextNode("second", TextType.LINKS_TEXT, "url2")
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_no_links(self):
        node = TextNode("Just plain text with no links.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_link_ignores_images(self):
        # A link parser should ignore image syntax (exclamation point prefix)
        node = TextNode("This is an ![image](img.png) not a link.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])


    # --- Complex Combined Test Cases ---

    def test_split_multiple_nodes_input(self):
        nodes = [
            TextNode("Text with [link](url)", TextType.PLAIN_TEXT),
            TextNode("Bold non-plain text", TextType.LINKS_TEXT, "url")
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINKS_TEXT, "url"),
            TextNode("Bold non-plain text", TextType.LINKS_TEXT, "url")
        ]
        self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()