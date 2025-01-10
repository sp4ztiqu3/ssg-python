import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

    def test_props_none(self):
        node = HTMLNode()
        self.assertNotEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(f"{node}", "HTMLNode(None, None, None, None)")

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_no_value(self):
        node = LeafNode(tag=None, value=None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_node_no_tag(self):
        node = LeafNode(tag=None, value="normal text")
        self.assertEqual(node.to_html(), "normal text")

    def test_leaf_node_p_tag(self):
        node = LeafNode(tag="p", value="hello world")
        self.assertEqual(node.to_html(), "<p>hello world</p>")

    def test_leaf_node_a_tag(self):
        node = LeafNode(tag="a", value="link text", props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://google.com" target="_blank">link text</a>')

class TestParentNode(unittest.TestCase):
    def test_single_child(self):
        node = ParentNode("p", [LeafNode("b", "bold text")])
        self.assertEqual(node.to_html(), "<p><b>bold text</b></p>")

    def test_multi_child(self):
        node = ParentNode("p", [LeafNode("b", "bold text"), LeafNode("i", "italic text"), LeafNode(None, "normal text")])
        self.assertEqual(node.to_html(), "<p><b>bold text</b><i>italic text</i>normal text</p>")

    def test_parent_children(self):
        node = ParentNode("p", [ParentNode("p1", [LeafNode("b", "bold text 1"), LeafNode("i", "italic text 1")]), ParentNode("p2", [LeafNode("b", "bold text 2")])])
        self.assertEqual(node.to_html(), "<p><p1><b>bold text 1</b><i>italic text 1</i></p1><p2><b>bold text 2</b></p2></p>")

    def test_parent_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_parent_no_tag(self):
        node = ParentNode(None, "test")
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
