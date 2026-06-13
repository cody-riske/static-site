import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_2(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is not a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_3(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, url = "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, url = None)
        self.assertNotEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_conversion(self):
        node = TextNode("Hello, world!", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, world!")

    def test_bold_conversion(self):
        node = TextNode("Bold content", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold content")

    def test_italic_conversion(self):
        node = TextNode("Italic content", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic content")

    def test_code_conversion(self):
        node = TextNode("print('hello')", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link_conversion(self):
        node = TextNode("Click here", TextType.LINKS_TEXT, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image_conversion(self):
        node = TextNode("A cute cat", TextType.IMAGES_TEXT, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com", "alt": "A cute cat"})

    def test_invalid_type_raises_error(self):
        # Create a dummy node with an invalid type string to trigger the exception catch-all
        node = TextNode("Bad node", "NOT_A_VALID_ENUM_TYPE")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()