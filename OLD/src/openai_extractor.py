import requests

from codeblock_extractor import extract_codeblock

url = "https://github.com/openai/openai-python/blob/main/README.md?raw=true"

response = requests.get(url)
codeblocks = extract_codeblock(response.text)


with open("example.py", "a") as f:
    for cb in codeblocks:
        f.write(cb + "\n")
        f.write(f"# {"-"*30}\n\n")
