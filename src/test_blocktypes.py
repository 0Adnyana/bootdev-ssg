from textwrap import dedent
import unittest

from blocktypes import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockTypes(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = dedent("""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_heading_1(self):
        block = "# Heading 1"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_heading_2(self):
        block = "## Heading 2"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_heading_3(self):
        block = "### Heading 3"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_heading_4(self):
        block = "#### Heading 4"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_heading_5(self):
        block = "##### Heading 5"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_heading_6(self):
        block = "###### Heading 6"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_not_heading_1(self):
        block = "#Heading 1"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_not_heading_2(self):
        block = "##Heading 2"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_not_heading_3(self):
        block = "###Heading 3"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_not_heading_4(self):
        block = "####Heading 4"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_not_heading_5(self):
        block = "#####Heading 5"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_not_heading_6(self):
        block = "######Heading 6"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_not_heading_7(self):
        block = "####### Heading 7"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.heading
        )

    def test_block_to_paragraph_invalid_heading(self):
        block = "####### Heading 7"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.paragraph
        )

    def test_block_to_code_single_line(self):
        block = "```\nprint('hello')\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_code_multi_line(self):
        block = "```\nline1\nline2\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_code_empty(self):
        block = "```\n\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_code_indented(self):
        block = "```\n  indented\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_code_with_comment(self):
        block = "```\n# comment\nx = 1\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_code_blank_line_inside(self):
        block = "```\na\n\nb\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_not_code_missing_opening_newline(self):
        block = "```code\n```"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_not_code_missing_closing_fence(self):
        block = "```\ncode"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_not_code_language_tag(self):
        block = "```python\ncode\n```"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_not_code_inline_backticks(self):
        block = "`code`"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_not_code_incomplete_opening_fence(self):
        block = "```"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_not_code_wrong_closing_fence(self):
        block = "```\ncode\n``"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_not_code_opening_fence_only(self):
        block = "```\n"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.code
        )

    def test_block_to_paragraph_code_with_language_tag(self):
        block = "```python\ncode\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.paragraph
        )

    def test_block_to_quote_single_line(self):
        block = "> quote"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_quote_multi_line(self):
        block = "> line1\n> line2"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_quote_empty_content(self):
        block = ">"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_quote_with_space(self):
        block = "> quote text"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_quote_three_lines(self):
        block = "> a\n> b\n> c"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_quote_no_space_after_gt(self):
        block = ">quote"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_not_quote_missing_gt_first_line(self):
        block = "quote"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_not_quote_missing_gt_second_line(self):
        block = "> line1\nline2"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_not_quote_mixed_lines(self):
        block = "> line1\nnot quote"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_not_quote_leading_space(self):
        block = " > quote"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_not_quote_middle_line_breaks(self):
        block = "> a\nb\n> c"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_not_quote_empty_block(self):
        block = ""
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_not_quote_gt_in_middle(self):
        block = "line\n> quote"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.quote
        )

    def test_block_to_paragraph_quote_missing_gt_second_line(self):
        block = "> line1\nline2"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.paragraph
        )

    def test_block_to_unordered_list_single_item(self):
        block = "- item"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_unordered_list_multi_line(self):
        block = "- item1\n- item2"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_unordered_list_three_items(self):
        block = "- a\n- b\n- c"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_unordered_list_empty_content(self):
        block = "- "
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_unordered_list_with_special_chars(self):
        block = "- **bold** item"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_unordered_list_long_list(self):
        block = "- one\n- two\n- three\n- four"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_not_unordered_list_missing_dash_first_line(self):
        block = "item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_not_unordered_list_missing_dash_second_line(self):
        block = "- item1\nitem2"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_not_unordered_list_mixed_lines(self):
        block = "- item1\nnot list"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_not_unordered_list_leading_space(self):
        block = " - item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_not_unordered_list_no_space_after_dash(self):
        block = "-item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_not_unordered_list_middle_line_breaks(self):
        block = "- a\nb\n- c"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_not_unordered_list_empty_block(self):
        block = ""
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_not_unordered_list_dash_in_middle(self):
        block = "line\n- item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.unordered_list
        )

    def test_block_to_paragraph_unordered_list_missing_dash_second_line(self):
        block = "- item1\nitem2"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.paragraph
        )

    def test_block_to_ordered_list_single_item(self):
        block = "1. item"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_ordered_list_two_items(self):
        block = "1. item1\n2. item2"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_ordered_list_three_items(self):
        block = "1. a\n2. b\n3. c"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_ordered_list_long_list(self):
        block = "1. one\n2. two\n3. three\n4. four"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_ordered_list_empty_content(self):
        block = "1. "
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_ordered_list_with_special_chars(self):
        block = "1. **bold** item"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_missing_number_first_line(self):
        block = "item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_missing_number_second_line(self):
        block = "1. item1\nitem2"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_wrong_second_number(self):
        block = "1. item1\n3. item2"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_mixed_lines(self):
        block = "1. item1\nnot list"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_leading_space(self):
        block = " 1. item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_no_space_after_dot(self):
        block = "1.item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_middle_line_breaks_sequence(self):
        block = "1. a\n2. b\n4. d"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_starts_with_two(self):
        block = "2. item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_not_ordered_list_number_in_middle(self):
        block = "line\n1. item"
        block_type = block_to_block_type(block)

        self.assertNotEqual(
            block_type,
            BlockType.ordered_list
        )

    def test_block_to_paragraph_ordered_list_missing_number_second_line(self):
        block = "1. item1\nitem2"
        block_type = block_to_block_type(block)

        self.assertEqual(
            block_type,
            BlockType.paragraph
        )

