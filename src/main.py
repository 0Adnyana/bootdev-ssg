from textnode import TextNode, TextType

print("Hello World")

test_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")


print(test_node)
