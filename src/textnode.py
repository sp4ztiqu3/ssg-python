from enum import Enum

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
