import os
import shutil
from markdown_to_html import *


def clear_and_create_public():
    source = "static"
    destination = "public"

    try:
        shutil.rmtree(destination)
    except FileNotFoundError:
        pass
    
    copy_files(source, destination)
         

def copy_files(source, destination):
    os.mkdir(destination)
    contents = os.listdir(source)
    for content in contents:
        src_path = os.path.join(source, content)
        dst_path = os.path.join(destination, content)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_files(src_path, dst_path)
