from textnode import TextType, block_to_block_type, markdown_to_blocks, text_to_textnodes

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        print(self)
        if self.props is not None:
            out = ""
            for key in self.props:
                out += f' {key}="{self.props[key]}"'
            return out #f' href="{self.props["href"]}" target="{self.props["target"]}"'
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        return f'<{self.tag}{self.props_to_html() if self.props is not None else ""}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("missing tag value")
        if self.children == None:
            raise ValueError("missing child node(s)")

        children_string = ""
        for child in self.children:
            children_string += child.to_html()

        return f'<{self.tag}{self.props if self.props is not None else ""}>{children_string}</{self.tag}>'

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url, "target": "_self" })
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("text node has invalid text_type")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        print(block)
        blocktype = block_to_block_type(block)
        print(blocktype)
        children += text_to_children(block, blocktype)
    parent = ParentNode("div", children)
    return parent


def text_to_children(text, blocktype):
    outputnodes = []
    match blocktype:
        case "paragraph":
            textnodes = text_to_textnodes(text)
            htmlnodes = []
            for node in textnodes:
                htmlnodes.append(text_node_to_html_node(node))
            outputnodes += htmlnodes
        case "heading":
            htmlnode = LeafNode("h1", text.split("# ",1)[1])
            outputnodes += [htmlnode]
        case "code":
            textnodes = text_to_textnodes(text)
            htmlnodes = []
            for node in textnodes:
                htmlnodes.append(text_node_to_html_node(node))
            outputnodes += htmlnodes
        case "quote":
            parsed = "\n".join(list(map(lambda l: l.split("> ",1)[1], text.split("\n"))))
            outputnodes += [LeafNode("blockquote", parsed)]
        case "unordered_list":
            parsed = ""
            if text[0] == "-":
                parsed = "\n".join(list(map(lambda l: l.split("- ",1)[1], text.split("\n"))))
            else:
                parsed = "\n".join(list(map(lambda l: l.split("* ",1)[1], text.split("\n"))))
            print(parsed)
            if parsed == "":
                # bad list, treat as paragraph
                return text_to_children(text, "paragraph")
            children = []
            for line in parsed.split("\n"):
                textnodes = text_to_textnodes(line)
                linehtmlnodes = []
                for node in textnodes:
                    linehtmlnodes.append(text_node_to_html_node(node))
                children.append(ParentNode("li", children = linehtmlnodes))
            outputnodes += [ParentNode("ul", children = children)]
        case "ordered_list":
            parsed = "\n".join(list(map(lambda l: l.split(". ",1)[1], text.split("\n"))))
            children = []
            for line in parsed.split("\n"):
                textnodes = text_to_textnodes(line)
                linehtmlnodes = []
                for node in textnodes:
                    linehtmlnodes.append(text_node_to_html_node(node))
                children.append(ParentNode("li", children = linehtmlnodes))
            outputnodes += [ParentNode("ul", children = children)]

    return outputnodes

