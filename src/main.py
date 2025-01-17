from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_images, split_nodes_link
from htmlnode import markdown_to_html_node


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

    split_nodes = split_nodes_delimiter([TextNode("ok *this* is a test", TextType.NORMAL)], "*", TextType.ITALIC)
    print(split_nodes)
    print("*this* is a test".split("*"))

    split_nodes = split_nodes_delimiter([TextNode("ok *this* is *a* test", TextType.NORMAL)], "*", TextType.ITALIC)
    print(split_nodes)

    split_nodes = split_nodes_delimiter(split_nodes_delimiter([TextNode("ok *this* is `a` test", TextType.NORMAL)], "*", TextType.ITALIC),"`", TextType.CODE)
    print(split_nodes)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))

    node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL)
    print(split_nodes_images([node]))

    node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
    print(split_nodes_link([node]))
    
    text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
    html = markdown_to_html_node(text)
    print(html)

if __name__ == "__main__":
    main()
