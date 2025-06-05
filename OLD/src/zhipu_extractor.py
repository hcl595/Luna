import json
from pathlib import Path
from urllib.parse import urlparse

import requests

from codeblock_extractor import extract_codeblock

# product name -> id json
query_for_dsply_json = Path.cwd() / "queryForDsply.json"
data = {}

if query_for_dsply_json.exists() is False:
    response = requests.get("https://bigmodel.cn/api/biz/platformDevDoc/queryForDsply")
    with open("queryForDsply.json", "wb") as f:
        f.write(response.content)
    data = response.json()
else:
    data = json.loads(query_for_dsply_json.read_bytes())

api_docs = data["data"][2]["children"][1]  # 接口文档-开放接口
path_to_id: dict[str, int] = {}

for i in api_docs["children"]:  # eg 语言模型
    for j in i["children"]:  # eg GLM-4 系列
        path_to_id[j["path"]] = j["meta"]["markdownZhId"]

input_url = "https://bigmodel.cn/dev/api/normal-model/glm-4"
base_url = "https://bigmodel.cn/api/biz/platformDevDoc/markdown/query?id={}"
url = base_url.format(path_to_id[urlparse(input_url).path])
response = requests.get(url)  # json

codeblocks = extract_codeblock(response.json()["data"])

with open("example.py", "a") as f:
    for cb in codeblocks:
        f.write(cb + "\n")
        f.write(f"# {"-"*30}\n\n")
