import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "hello")
        node2 = HTMLNode("h1", "hello")

        return self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="this is a link with props",
            props={"class": "google_link", "href": "https://google.com"},
        )

        return self.assertEqual(
            node.props_to_html(), ' class="google_link" href="https://google.com"'
        )

    def test_tag_none(self):
        node = HTMLNode(value="Hey there how are you?")

        return self.assertEqual(node.tag, None)

    def test_value_none(self):
        child = HTMLNode(tag="h1", value="hello")
        parent = HTMLNode(tag="a", children=[child], props={"href": "/home"})

        return self.assertEqual(parent.value, None)

    def test_children_none(self):
        node = HTMLNode(tag="h1", value="hello")

        return self.assertEqual(node.children, None)

    def test_props_none(self):
        node = HTMLNode(tag="h1", value="hello")
        return self.assertEqual(node.props, None)
