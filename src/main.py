from textnode import TextNode, TextType, split_nodes_delimiter


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

if __name__ == "__main__":
    main()
