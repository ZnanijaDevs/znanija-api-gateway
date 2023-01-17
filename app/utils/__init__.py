import re


def filter_node_content(content: str) -> str:
    """Filter a content of question/answer"""
    filtered_content = content

    replacements = [
        (r"<br\s\/>", "\n"),
        (r"<\/?\w+\s?\/?>", ""),
        (r"\n{2,}|\n\s*\n", "\n"),
        (r"^(\s|\n)|(\s?\n)$", "")
    ]

    for regex, new in replacements:
        filtered_content = re.sub(regex, new, filtered_content)

    filtered_content = filtered_content.strip()

    return filtered_content
