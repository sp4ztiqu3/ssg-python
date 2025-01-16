from enum import Enum
import re

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) == 1:
            new_nodes.append(node)
            continue
        elif not len(split_text) % 2:
            raise Exception("odd number of delimiters found")

        for (i, text) in enumerate(split_text):
            if not i % 2:
                new_nodes.append(TextNode(text, TextType.NORMAL))
            else:
                new_nodes.append(TextNode(text, text_type))
    
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        results = extract_markdown_images(node.text)
        if results == []:
            new_nodes.append(node)
            continue

        text = node.text
        for result in results:
            sections = text.split(f"![{result[0]}]({result[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(result[0], TextType.IMAGE, result[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        results = extract_markdown_links(node.text)
        if results == []:
            new_nodes.append(node)
            continue

        text = node.text
        for result in results:
            sections = text.split(f"[{result[0]}]({result[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(result[0], TextType.LINK, result[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_images(split_nodes_link([TextNode(text, TextType.NORMAL)])),"**",TextType.BOLD),"*", TextType.ITALIC),"`",TextType.CODE)

def markdown_to_blocks(markdown):
    blocks = []
    sections = []
    sections = markdown.split("\n\n")
    for section in sections:
        if section.strip() != "":
            blocks.append(section.strip())
    return blocks

def block_to_block_type(block):
    if block[:2] == "# " or block[:3] == "## " or block[:4] == "### " or block[:5] == "#### " or block[:6] == "##### " or block[:7] == "###### ":
        return "heading"
    if block[:3] == "```" and block[-3:] == "```":
        return "code"
    if block[0] == ">":
        for line in block.split("\n"):
            if line[0] != ">":
                return "paragraph"
        return "quote"
    if block[:2] == "* ":
        for line in block.split("\n"):
            if line[:2] != "* ":
                return "paragraph"
        return "unordered_list"
    if block[:2] == "- ":
        for line in block.split("\n"):
            if line[:2] != "- ":
                return "paragraph"
        return "unordered_list"
    if block[0].isdigit():
        for line in block.split("\n"):
            if not ". " in line:
                return "paragraph"
            sections = line.split(". ", 1)
            for char in sections[0]:
                if not char.isdigit():
                    return "paragraph"
        return "ordered_list"
    return "paragraph"

