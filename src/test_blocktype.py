import unittest
from blocktype import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        # Plain text
        block = "This is a normal paragraph block with multiple lines.\nIt does not match any special markdown syntax."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_headings(self):
        # Valid headings 1 to 6
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Invalid heading (7 hashes) -> Paragraph
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)
        # Invalid heading (No space) -> Paragraph
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        # Valid multiline code block
        block = "```\ndef my_func():\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Invalid code block (Missing the immediate newline) -> Paragraph
        invalid_block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(invalid_block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        # Valid quotes (with and without spaces)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Line 1\n> Line 2\n>Line 3"), BlockType.QUOTE)
        
        # Invalid quote (One line missing the character) -> Paragraph
        invalid_block = "> Line 1\nLine 2 without angle bracket"
        self.assertEqual(block_to_block_type(invalid_block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        # Valid unordered list
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
        # Invalid unordered list (Missing space) -> Paragraph
        invalid_block = "- Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(invalid_block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Valid ordered list starting at 1 and incrementing correctly
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        
        # Invalid ordered list (Does not start at 1) -> Paragraph
        invalid_start = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(invalid_start), BlockType.PARAGRAPH)
        
        # Invalid ordered list (Broken sequence) -> Paragraph
        invalid_sequence = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(invalid_sequence), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()