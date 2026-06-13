import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        # Test a standard case with multiple attributes
        node = HTMLNode(
            tag="a", 
            value="Link", 
            props={"href": "https://google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://google.com" target="_blank"'
        )

    def test_props_to_html_with_single_prop(self):
        # Test a case with only one attribute
        node = HTMLNode(tag="p", value="Text", props={"class": "paragraph"})
        self.assertEqual(node.props_to_html(), ' class="paragraph"')

    def test_props_to_html_with_no_props(self):
        # Test that None or empty dictionary returns an empty string
        node1 = HTMLNode(tag="h1", value="Header", props=None)
        node2 = HTMLNode(tag="h1", value="Header", props={})
        
        self.assertEqual(node1.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), "")

    def test_leaf_to_html_p(self):
    # Test standard paragraph rendering
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_to_html_link(self):
        # Test rendering with attributes
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertEqual(
            node.to_html(), 
            '<a href="https://google.com">Click me!</a>'
        )

    def test_leaf_to_html_raw_text(self):
        # Test that None tag renders as raw text
        node = LeafNode(None, "Just raw text.")
        self.assertEqual(node.to_html(), "Just raw text.")

    def test_leaf_to_html_missing_value(self):
        # Test that a ValueError is raised if value is missing
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_with_leaf_children(self):
    # Test standard case with multiple LeafNode children
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_parent_to_html_with_nested_parents(self):
        # Test deep nesting: ParentNode inside another ParentNode
        nested_node = ParentNode(
            "div",
            [
                LeafNode("span", "Nested child"),
            ]
        )
        root_node = ParentNode(
            "body",
            [nested_node, LeafNode("p", "Sibling child")]
        )
        self.assertEqual(
            root_node.to_html(),
            "<body><div><span>Nested child</span></div><p>Sibling child</p></body>"
        )

    def test_parent_to_html_with_props(self):
        # Test that a ParentNode correctly renders its own attributes
        node = ParentNode(
            "div",
            [LeafNode("p", "Content")],
            {"class": "container", "id": "main"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><p>Content</p></div>'
        )

    def test_parent_to_html_missing_tag(self):
        # Edge case: Missing tag raises ValueError
        node = ParentNode(None, [LeafNode("span", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_missing_children(self):
        # Edge case: Children is None raises ValueError
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_empty_children_list(self):
        # Edge case: Children list is empty (should render tags with nothing inside)
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

if __name__ == "__main__":
    unittest.main()