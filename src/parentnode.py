from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag,
        children,
        props=None,
    ):
        super().__init__(tag=tag, value=None, props=props, children=children)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is empty")

        if not self.children:
            raise ValueError("Children cannot be empty")

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"

        child_string = []

        for child in self.children:
            child_string.append(child.to_html())

        return f"{opening_tag}{''.join(child_string)}{closing_tag}"
