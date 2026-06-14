import re
from enum import Enum


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
    if re.match("^#{1,6} .+", text):
        return BlockType.heading

    if text.startswith("```\n") and text.endswith("```"):
        return BlockType.code

    lines = text.split("\n")
    if lines[0].startswith(">"):
        is_quote = True
        for t in lines[1::]:
            if not t.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.quote
    
    if lines[0].startswith("- "):
        is_list = True
        for t in lines[1::]:
            if not t.startswith("- "):
                is_list = False
                break
        if is_list:
            return BlockType.unordered_list

    number = 1
    if lines[0].startswith(f"{number}. "):
        is_num_list = True
        for t in lines[1::]:
            if not t.startswith(f"{number+1}. "):
                is_num_list = False
                break
            number += 1
        if is_num_list:
            return BlockType.ordered_list

    return BlockType.paragraph