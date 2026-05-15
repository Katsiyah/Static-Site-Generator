from block_markdown import *
from inline_markdown import *
from textnode import *
from htmlnode import *


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    new_blocks = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = ""
        if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
            node = ParentNode(get_html_tag(block_type), wrap_list_in_li(block, block_type))

        elif block_type == BlockType.CODE:
            code_text_node = text_node_to_html_node(TextNode(remove_block_prefixes(block, block_type), TextType.TEXT))
            code_node = ParentNode(get_html_tag(block_type), [code_text_node])
            node = ParentNode("pre", [code_node])

        else:
            # headings, quotes, paragraphs
            node = ParentNode(get_html_tag(block_type, block), text_to_children(remove_block_prefixes(block, block_type)))
            
        new_blocks.append(node)

    div_block = ParentNode("div", new_blocks)
    return div_block


def get_html_tag(block_type, block=None):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"

        case BlockType.HEADING:
            prefix, text = block.split(" ", 1)
            return f"h{len(prefix)}"

        case BlockType.CODE:
            return "code"

        case BlockType.QUOTE:
            return "blockquote"

        case BlockType.UNORDERED_LIST:
            return "ul"

        case BlockType.ORDERED_LIST:
            return "ol"
        
        case _:
            return


def remove_block_prefixes(text, block_type):
    stripped = ""
    if block_type == BlockType.PARAGRAPH:
        stripped = text.replace("\n", " ")
    
    elif block_type == BlockType.QUOTE:
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            stripped = line.lstrip(">").strip()
            new_lines.append(stripped)
        stripped = " ".join(new_lines)

    elif block_type == BlockType.CODE:
        lines = text.split("\n")
        code_lines = lines[1:-1]
        stripped = "\n".join(code_lines) + "\n"
    else:
        # headings & lists
        split_text = text.split(" ", 1)
        stripped = split_text[1]

    return stripped


def wrap_list_in_li(block_lines, block_type):
    lines = block_lines.split("\n")
    li_lines = []
    for line in lines:
        node = ParentNode("li", text_to_children(remove_block_prefixes(line, block_type)))
        li_lines.append(node)
    return li_lines


def text_to_children(text):
    children = text_to_textnodes(text)
    child_nodes = []
    for child in children:
        child_nodes.append(text_node_to_html_node(child))
    return child_nodes