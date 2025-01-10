import unittest

from htmlnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is an italix node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.NORMAL, "htto://www.google.com")
        node2 = TextNode("This is a text node", TextType.NORMAL, "http://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text_to_html_normal(self):
        node = TextNode("normal text", TextType.NORMAL)
        self.assertEqual(text_node_to_html_node(node), LeafNode(None, "normal text"))

    def test_text_to_html_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node), LeafNode("b", "bold text"))

    def test_text_to_html_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node), LeafNode("i", "italic text"))

    def test_text_to_html_code(self):
        node = TextNode("code text", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node), LeafNode("code", "code text"))

    def test_text_to_html_link(self):
        node = TextNode("link text", TextType.LINK, url="https://www.google.com")
        self.assertEqual(text_node_to_html_node(node), LeafNode("a", "link text", {"href": "https://www.google.com"}))

    def test_text_to_html_image(self):
        node = TextNode("image text", TextType.IMAGE, url="test_image.png")
        self.assertEqual(text_node_to_html_node(node), LeafNode("img", "", {"src": "test_image.png", "alt": "image text"}))

    def test_split_delimiter_single(self):
        node = TextNode("this should be **BOLD** text", TextType.NORMAL)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, [TextNode("this should be ", TextType.NORMAL), TextNode("BOLD", TextType.BOLD), TextNode(" text", TextType.NORMAL)])

    def test_split_delimiter_nested(self):
        node = TextNode("normal *italic* normal **bold** normal `code` normal", TextType.NORMAL)
        split_nodes = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([node], "**", TextType.BOLD), "*", TextType.ITALIC), "`", TextType.CODE)
        correct_split = [TextNode("normal ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" normal ", TextType.NORMAL), TextNode("bold", TextType.BOLD), TextNode(" normal ", TextType.NORMAL), TextNode("code", TextType.CODE), TextNode(" normal", TextType.NORMAL)]
        self.assertEqual(split_nodes, correct_split)

if __name__ == "__main__":
    unittest.main()
