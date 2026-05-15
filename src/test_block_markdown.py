import unittest

from block_markdown import *


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    
    def test_markdown_to_blocks_leading_trailing(self):
        md = "block one       \n\n       block two      "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "block one", "block two"
            ],
            blocks
        )


    def test_markdown_to_blocks_only_whitespace(self):
        md = "block one\n\n       \n\nblock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "block one", "block two"
            ],
            blocks
        )


    def test_markdown_to_blocks_single(self):
        md = "block one"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "block one"
            ],
            blocks
        )
    

    def test_markdown_to_blocks_leading_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [],
            blocks
        )

    
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)


    def test_block_to_block_type_heading_3(self):
        block = "### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    
    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)
    

    def test_block_to_block_type_code_empty(self):
        block = "```\n\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)    


    def test_block_to_block_type_quote(self):
        block = "> this is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)


    def test_block_to_block_type_quote_multiline(self):
        block = "> this is a quote\n> This is a second quote"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)


    def test_block_to_block_type_unordered_list(self):
        block = "- this is a list item\n- this is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)


    def test_block_to_block_type_ordered_list(self):
        block = "1. this is a list item\n2. this is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)


    def test_block_to_block_type_incorrect(self):
        heading = "###this is a heading"
        code = "```\nthis is a code block```"
        quote = ">this is a quote\nThis is a second quote"
        unordered = "- this is a list item\n-this is another list item"
        ordered = "3. this is a list item\n2. this is another list item"
        results = [
            block_to_block_type(heading),
            block_to_block_type(code),
            block_to_block_type(quote),
            block_to_block_type(unordered),
            block_to_block_type(ordered),
        ]
        self.assertEqual([
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            ], results)