import unittest
from textnode import *
from inline_markdown import *


class TestInline(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" word", TextType.TEXT),
                        ], new_nodes)
    
    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("bold", TextType.BOLD),
                        TextNode(" word", TextType.TEXT),
                        ], new_nodes)

    
    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual([
                        TextNode("This is text with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word", TextType.TEXT),
                        ], new_nodes)
    

    def test_code_delimiter_start(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([
                        TextNode("code block", TextType.CODE),
                        TextNode(" word", TextType.TEXT),
                        ], new_nodes)


    def test_code_delimiter_unmatched(self):
        node = TextNode("`code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_code_delimiter_not_text(self):
        node = TextNode("`code block` word", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([TextNode("`code block` word", TextType.CODE)], new_nodes)

    def test_code_delimiter_none(self):
        node = TextNode("code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([
                        TextNode("code block word", TextType.TEXT),
                        ], new_nodes)


    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italic_ word and _multiple_ delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual([
                        TextNode("This is text with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and ", TextType.TEXT),
                        TextNode("multiple", TextType.ITALIC),
                        TextNode(" delimiters", TextType.TEXT)
                        ], new_nodes)
    

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
    

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
            "This is text with an no image or link"
        )
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "This is text with an no image or link"
        )
        self.assertListEqual([], matches)
    

    def test_extract_markdown_images_partial(self):
        matches = extract_markdown_images(
            "This is text with an no ![image] or link"
        )
        self.assertListEqual([], matches)


    def test_extract_markdown_links_partial(self):
        matches = extract_markdown_links(
            "This is text with an no [image]( or link"
        )
        self.assertListEqual([], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )



    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )





    def test_split_links_at_start(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_images_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_links_none(self):
        node = TextNode(
            "no link :(",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("no link :(", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_images_none(self):
        node = TextNode(
            "no image :(",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("no image :(", TextType.TEXT),
            ],
            new_nodes,
        )



    def test_text_to_textnodes_all_types(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], nodes)

    def test_text_to_textnodes_plain(self):
        nodes = text_to_textnodes("This is a plain string")
        self.assertEqual([TextNode("This is a plain string", TextType.TEXT)], nodes)

    def test_text_to_textnodes_one_type(self):
        nodes = text_to_textnodes("This is a plain string with only **BOLD**")
        self.assertEqual(
            [
                TextNode("This is a plain string with only ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD)
            ], nodes)

    def test_text_to_textnodes_one_type_empty(self):
        nodes = text_to_textnodes("This is a plain string with only ****")
        self.assertEqual(
            [
                TextNode("This is a plain string with only ", TextType.TEXT)
            ], nodes)

    def test_text_to_textnodes_unclosed(self):
        with self.assertRaises(ValueError):
            nodes = text_to_textnodes("This is a plain string with only **BOLD")
        
    
    def test_text_to_textnodes_two_same(self):
        nodes = text_to_textnodes("This is a plain string with **only** 2 **BOLD** sections")
        self.assertEqual(
            [
                TextNode("This is a plain string with ", TextType.TEXT),
                TextNode("only", TextType.BOLD),
                TextNode(" 2 ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode(" sections", TextType.TEXT)
            ], nodes)