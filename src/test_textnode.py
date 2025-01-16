import unittest

from htmlnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType, block_to_block_type, extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_delimiter, split_nodes_images, split_nodes_link, text_to_textnodes


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

    def test_extract_md_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_md_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_md_images_none(self):
        text = "No images here"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_md_links_none(self):
        text = "No links here"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_split_images(self):
        text = "Here is an image: ![alt text](www.url.com/image.jpg)"
        node = TextNode(text, TextType.NORMAL)
        self.assertEqual(split_nodes_images([node]), [TextNode("Here is an image: ", TextType.NORMAL), TextNode("alt text", TextType.IMAGE, "www.url.com/image.jpg")])

    def test_split_links(self):
        text = "Here is an link: [link text](www.url.com)"
        node = TextNode(text, TextType.NORMAL)
        self.assertEqual(split_nodes_link([node]), [TextNode("Here is an link: ", TextType.NORMAL), TextNode("link text", TextType.LINK, "www.url.com")])

    def test_split_image_and_links(self):
        text = "Here is a link: [link text](www.url.com) and an image ![alt text](www.url.com/image.jpg) more text"
        node = TextNode(text, TextType.NORMAL)
        self.assertEqual(split_nodes_link(split_nodes_images([node])), [TextNode("Here is a link: ", TextType.NORMAL), TextNode("link text", TextType.LINK, "www.url.com"), TextNode(" and an image ", TextType.NORMAL), TextNode("alt text", TextType.IMAGE, "www.url.com/image.jpg"), TextNode(" more text", TextType.NORMAL)])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, text_to_textnodes(text))

    def test_markdown_to_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(result, markdown_to_blocks(text))

    def test_heading_blocks(self):
        self.assertEqual(block_to_block_type("# Heading"), "heading")
        self.assertEqual(block_to_block_type("## Heading"), "heading")
        self.assertEqual(block_to_block_type("### Heading"), "heading")
        self.assertEqual(block_to_block_type("#### Heading"), "heading")
        self.assertEqual(block_to_block_type("##### Heading"), "heading")
        self.assertEqual(block_to_block_type("###### Heading"), "heading")

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```code```"), "code")

    def test_quote_block(self):
        self.assertEqual(block_to_block_type(">quote"), "quote")

    def test_multiline_quote_block(self):
        self.assertEqual(block_to_block_type(">quote\n> quote\n>quote"), "quote")

    def test_unordered_list_star(self):
        self.assertEqual(block_to_block_type("* item\n* item 2"), "unordered_list")

    def test_unordered_list_dash(self):
        self.assertEqual(block_to_block_type("- item\n- item 2"), "unordered_list")

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item\n2. item\n999. item"), "ordered_list")

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("test"), "paragraph")

    def test_bad_blocks(self):
        self.assertEqual(block_to_block_type("#heading"), "paragraph")
        self.assertEqual(block_to_block_type("``code``"), "paragraph")
        self.assertEqual(block_to_block_type(">quote\nquote"), "paragraph")
        self.assertEqual(block_to_block_type("* list\n*list"), "paragraph")
        self.assertEqual(block_to_block_type("- list\n* list"), "paragraph")
        self.assertEqual(block_to_block_type("1. list\nlist"), "paragraph")


if __name__ == "__main__":
    unittest.main()
