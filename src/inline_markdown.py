import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        temp_strings = node.text.split(delimiter)
        if len(temp_strings) % 2 == 0:
            raise ValueError("invalid Markdown syntax")
        
        for i in range(len(temp_strings)):
            if temp_strings[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(temp_strings[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(temp_strings[i], text_type))

    return new_nodes



def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        for match in matches:
            image_alt, image_link = match
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
    
            if sections[0] == "":
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            else:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            text = sections[1]
        
        if text == "":
            continue
        new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes




def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        for match in matches:
            link_alt, link = match
            sections = text.split(f"[{link_alt}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
    
            if sections[0] == "":
                new_nodes.append(TextNode(link_alt, TextType.LINK, link))
            else:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_alt, TextType.LINK, link))

            text = sections[1]
        
        if text == "":
            continue
        new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    new_node = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(new_node, "**", TextType.BOLD),
                     "_", TextType.ITALIC), "`", TextType.CODE)))
    return nodes