from enum import Enum

from leafnode import LeafNode
from utils import extract_markdown_images, extract_markdown_links


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "images"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return NotImplementedError

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("Invalid Text Type")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value=None,
                props={"src": text_node.url, "alt": text_node.text},
            )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) == 0:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid markdown syntax")

        parts = node.text.split(delimiter)

        for index, part in enumerate(parts):
            if not part:
                continue
            else:
                if index % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted = extract_markdown_images(node.text)

        if not extracted:
            new_nodes.append(node)
            continue

        parts = node.text
        for image_alt, image_link in extracted:
            parts = parts.split(f"![{image_alt}]({image_link})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(
                TextNode(text=image_alt, url=image_link, text_type=TextType.IMAGE)
            )

            parts = parts[1]

        if parts:
            new_nodes.append(TextNode(parts, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted = extract_markdown_links(node.text)

        if not extracted:
            new_nodes.append(node)
            continue

        parts = node.text
        for link_title, url in extracted:
            parts = parts.split(f"[{link_title}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(
                TextNode(text=link_title, url=url, text_type=TextType.LINK)
            )

            parts = parts[1]

        if parts:
            new_nodes.append(TextNode(parts, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)

    return split_nodes_link(nodes)
