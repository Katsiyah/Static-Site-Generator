import unittest
from markdown_to_html import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    
    def test_headings(self):
        md = "### This is a level 3 heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><h3>This is a level 3 heading</h3></div>", html
        )
    

    def test_quotes(self):
        md = ">This is a quote with\n>several lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><blockquote>This is a quote with several lines</blockquote></div>", html
        )


    def test_unordered_list(self):
        md = "- this is a list item\n- and another one"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ul><li>this is a list item</li><li>and another one</li></ul></div>", html
        )

    def test_ordered_list(self):
        md = "1. this is a list item\n2. and another one"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ol><li>this is a list item</li><li>and another one</li></ol></div>", html
        )