from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return BlockType.HEADING
    
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # 3. Quote Block Check (Every line starts with '>')
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # 4. Unordered List Check (Every line starts with '- ')
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # 5. Ordered List Check (Starts at 1. and increments by 1 on each line)
    is_ordered_list = True
    for index, line in enumerate(lines, start=1):
        if not line.startswith(f"{index}. "):
            is_ordered_list = False
            break
            
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    # 6. Default Fallback
    return BlockType.PARAGRAPH