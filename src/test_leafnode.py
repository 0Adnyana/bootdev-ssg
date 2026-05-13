import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_tag_none(self):
        node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(node.tag, None)

    def test_value_none(self):
        node = LeafNode(tag="h1", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_link_props(self):
        node = LeafNode(
            tag="a", value="hey there!", props={"href": "https://example.com"}
        )

        return self.assertIn("href", node.props)
