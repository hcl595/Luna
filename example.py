from zhipuai import ZhipuAI
client = ZhipuAI(api_key="")  # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4-plus",  # 请填写您要调用的模型名称
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的口号"},
        {"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"},
        {"role": "assistant", "content": "点燃未来，智谱AI绘制无限，让创新触手可及！"},
        {"role": "user", "content": "创作一个更精准且吸引人的口号"}
    ],
)
print(response.choices[0].message)

# ------------------------------

{
  "created": 1703487403,
  "id": "8239375684858666781",
  "model": "glm-4-plus",
  "request_id": "8239375684858666781",
  "choices": [
      {
          "finish_reason": "stop",
          "index": 0,
          "message": {
              "content": "以AI绘蓝图 — 智谱AI，让创新的每一刻成为可能。",
              "role": "assistant"
          }
      }
  ],
  "usage": {
      "completion_tokens": 217,
      "prompt_tokens": 31,
      "total_tokens": 248
  }
}

# ------------------------------

from zhipuai import ZhipuAI
client = ZhipuAI(api_key="")  # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4-plus",  # 请填写您要调用的模型名称
    messages=[
        {"role": "system", "content": "你是一个乐于回答各种问题的小助手，你的任务是提供专业、准确、有洞察力的建议。"},
        {"role": "user", "content": "我对太阳系的行星非常感兴趣，尤其是土星。请提供关于土星的基本信息，包括它的大小、组成、环系统以及任何独特的天文现象。"},
    ],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta)

# ------------------------------

from zhipuai import ZhipuAI

client = ZhipuAI(api_key="") # 请填写您自己的APIKey

tools = [
    {
        "type": "function",
        "function": {
            "name": "query_train_info",
            "description": "根据用户提供的信息查询火车时刻",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure": {
                        "type": "string",
                        "description": "出发城市或车站",
                    },
                    "destination": {
                        "type": "string",
                        "description": "目的地城市或车站",
                    },
                    "date": {
                        "type": "string",
                        "description": "要查询的火车日期",
                    },
                },
                "required": ["departure", "destination", "date"],
            },
        }
    }
]
messages = [
    {
        "role": "user",
        "content": "你能帮我查一下2024年1月1日从北京南站到上海的火车票吗？"
    }
]
response = client.chat.completions.create(
    model="glm-4-plus", # 请填写您要调用的模型名称
    messages=messages,
    tools=tools,
    tool_choice="auto",
)
print(response.choices[0].message)

# ------------------------------

{
  "id": "8231168139794583938",
  "model": "glm-4-plus",
  "request_id": "8231168139794583938",
  "created": 1703490288,
  "choices": [
      {
          "finish_reason": "tool_calls",
          "index": 0,
          "message": {
              "role": "assistant",
              "tool_calls": [
                  {
                      "id": "call_8231168139794583938",
                      "index": 0,
                      "type": "function",
                      "function": {
                          "arguments": '{"date": "2024-01-01","departure": "北京南站","destination": "上海"}',
                          "name": "query_train_info"
                      }
                  }
              ]
          }
      }
  ],
  "usage": {
      "completion_tokens": 31,
      "prompt_tokens": 120,
      "total_tokens": 151
  }
}

# ------------------------------

