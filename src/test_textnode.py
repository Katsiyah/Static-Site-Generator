import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_defaulturl(self):
        node = TextNode("This has no URL", TextType.TEXT)
        self.assertEqual(None, node.url)
    
    def test_repr(self):
        node  = TextNode("Hello", TextType.ITALIC)
        self.assertEqual("TextNode(Hello, italic, None)", repr(node))


if __name__ == "__main__":
    unittest.main()