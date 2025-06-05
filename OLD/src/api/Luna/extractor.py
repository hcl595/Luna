import ast
import requests
import mistune

def is_valid_python(code):
    try:
        ast.parse(code)
    except SyntaxError:
        return False
    return True

def extract_codeblock(markdown: str, *, only_python_code=True) -> list[str]:
    """extract code block from markdown"""
    ast = mistune.create_markdown(renderer="ast")(markdown)
    if isinstance(ast, str):
        return []
    raw_codeblocks = [
        element.get("raw", "") for element in ast if element.get("type") == "block_code"
    ]
    if only_python_code is False:
        return raw_codeblocks

    # filter out python code
    return [cb for cb in raw_codeblocks if is_valid_python(cb)]


def write_pyFile(url: str,path) -> list[str]:
    response = requests.get(url)
    codeblocks = extract_codeblock(response.text)
    with open(path, "a") as f:
        for cb in codeblocks:
            f.write(cb + "\n")
            f.write(f"# {"-"*30}\n\n")



