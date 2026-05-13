import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_tag_is_none(self):
        parent = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_tag_empty_string(self):
        parent = ParentNode("", [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_children_is_none(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_children_empty_list(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_with_props(self):
        parent = ParentNode(
            "div", [LeafNode("span", "child")], props={"class": "container"}
        )
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_multiple_children_order(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "first"),
                LeafNode("i", "second"),
                LeafNode("span", "third"),
            ],
        )
        self.assertEqual(
            parent.to_html(),
            "<p><b>first</b><i>second</i><span>third</span></p>",
        )

    def test_child_with_props(self):
        parent = ParentNode(
            "div",
            [
                LeafNode("a", "link", props={"href": "https://example.com"}),
            ],
        )
        self.assertEqual(
            parent.to_html(),
            '<div><a href="https://example.com">link</a></div>',
        )

    def test_plain_text_leaf_child(self):
        parent = ParentNode("div", [LeafNode(None, "plain text")])
        self.assertEqual(parent.to_html(), "<div>plain text</div>")
