import os
import shutil
import sys

from textnode import TextNode, TextType
from copystatic import copy_directory_recursive
from generate_page import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main() -> None:
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print("Copying static files to public directory...")
    # This automatically cleans and recreates public/ inside your custom implementation
    copy_directory_recursive(dir_path_static, dir_path_public)

    print("Generating all pages recursively...")
    # FIX: Replace the single generate_page call with the recursive crawler
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        basepath
    )
    
    print("Static site generation complete!")

if __name__ == "__main__":
    main()