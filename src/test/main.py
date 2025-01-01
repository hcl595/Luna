import jieba
import requests
from bs4 import BeautifulSoup

# url = "https://github.com/MetaGLM/zhipuai-sdk-python-v4"
url = "https://github.com/openai/openai-python"

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")
judge = True

codes = soup.find_all("pre")
for code in codes:
    if judge:
        seg_list = jieba.lcut_for_search(code.text)  # 搜索引擎模式
        # print(code.text)
        for seg in seg_list:
            # print(seg)
            if seg == "How":
                # print(", ".join(seg_list))
                print(code.text)
                # print("///////////")
                open("./src/test/aim.py", "a").write("\n" + code.text)
                judge = False
