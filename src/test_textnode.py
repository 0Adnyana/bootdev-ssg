import unittest

from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_not_exist(self):
        node = TextNode("This is a text node without url", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_texttype_not_eq(self):
        node = TextNode("This is a text node of type BOLD", TextType.BOLD)
        node2 = TextNode("This is a text node of type TEXT", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("hey i am node", TextType.BOLD)
        node2 = TextNode("this should differ from node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_conversion(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

    def test_italic_conversion(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)

    def test_code_conversion(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")
        self.assertIsNone(html_node.props)

    def test_link_conversion(self):
        url = "https://example.com"
        node = TextNode("click here", TextType.LINK, url=url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": url})

    def test_image_conversion(self):
        url = "https://example.com/image.png"
        node = TextNode("an image", TextType.IMAGE, url=url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props, {"src": url, "alt": "an image"})

    def test_invalid_text_type_raises(self):
        # text_type is not a member of TextType
        node = TextNode("bad", "NOT_A_TYPE")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_split_delimiter_bold(self):
        node = TextNode(
            "a random text that contains _italic_ and then **bold** texts. It also contains `code` texts too because it wants to be cool.",
            TextType.TEXT,
        )
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_outcome = [
            TextNode("a random text that contains _italic_ and then ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(
                " texts. It also contains `code` texts too because it wants to be cool.",
                TextType.TEXT,
            ),
        ]
        self.assertEqual(split_nodes, expected_outcome)

    def test_split_delimiter_italic(self):
        node = TextNode(
            "a random text that contains _italic_ and then **bold** texts. It also contains `code` texts too because it wants to be cool.",
            TextType.TEXT,
        )
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_outcome = [
            TextNode("a random text that contains ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(
                " and then **bold** texts. It also contains `code` texts too because it wants to be cool.",
                TextType.TEXT,
            ),
        ]
        self.assertEqual(split_nodes, expected_outcome)

    def test_split_delimiter_code(self):
        node = TextNode(
            "a random text that contains _italic_ and then **bold** texts. It also contains `code` texts too because it wants to be cool.",
            TextType.TEXT,
        )
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_outcome = [
            TextNode(
                "a random text that contains _italic_ and then **bold** texts. It also contains ",
                TextType.TEXT,
            ),
            TextNode("code", TextType.CODE),
            TextNode(
                " texts too because it wants to be cool.",
                TextType.TEXT,
            ),
        ]
        self.assertEqual(split_nodes, expected_outcome)

    def test_split_delimiter_multiple(self):
        """Test that all three inline types (italic, bold, code) are split when chaining delimiter splits."""
        node = TextNode(
            "a random text that contains _italic_ and then **bold** texts. It also contains `code` texts too because it wants to be cool.",
            TextType.TEXT,
        )
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        split_nodes = split_nodes_delimiter(split_nodes, "**", TextType.BOLD)
        split_nodes = split_nodes_delimiter(split_nodes, "_", TextType.ITALIC)
        expected_outcome = [
            TextNode("a random text that contains ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and then ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" texts. It also contains ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(
                " texts too because it wants to be cool.",
                TextType.TEXT,
            ),
        ]
        self.assertEqual(split_nodes, expected_outcome)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
