from enum import Enum
import re


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def markdown_to_blocks(text):
    stripped = list(map(lambda x: x.strip(), text.split("\n\n")))

    return list(filter(None, stripped))


def block_to_block_type(text: str):
    if text.startswith("# ", 0, 5):
        return BlockType.heading

    if text.startswith("```") and text.endswith("```"):
        return BlockType.code

    # need to check per line here.
    if text.startswith(">") or text.startswith("> "):
        return BlockType.quote

    if text.startswith("- "):
        return BlockType.unordered_list

    if text.startswith(r"\d.( )"):
        return BlockType.ordered_list
