import subprocess
import psutil
from concurrent.futures import ProcessPoolExecutor
from typing import TypedDict
import mistune
import requests
import json

class Message(TypedDict):
    role: str
    content: str

def request_OpenAI(APIKEY: str, ModelName:str, RequestURL:str, Userinput: str, historys: list,stream: bool):
    '''
    APIKEY    API KEY
    ModelName 模型名称
    Userinput 用户输入的内容
    stream    是否需要流式传输
    '''
    ##Universal
    #Setup
    messages = []
    response = ""
    
    #History
    for r in historys:
        question: Message = {"role": "user", "content": r[0]}
        response_model: Message = {"role": "assistant", "content": r[1]}
        messages.append(question)
        messages.append(response_model)
    
    #Check lib & auto install
    try:
        import openai
    except ImportError:
        with ProcessPoolExecutor() as p:
            try:
                p.submit(subprocess.run, "pip install "+"openai")
            except psutil.AccessDenied:
                raise ImportError("No moduel named"+"openai")

    ##Generated Code
    #Request ai
    try:
        question: Message = {"role": "user", "content": Userinput}
        messages.append(question)
        openai.api_key = APIKEY
        openai.api_base = RequestURL
        for chunk in openai.ChatCompletion.create(
            model=ModelName,
            messages=messages,
            stream=True,
            temperature=0,
        ):
            if stream == True:
                if hasattr(chunk.choices[0].delta, "content"):
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    response = response + chunk.choices[0].delta.content
                    response_out = mistune.html(response)
                    yield response_out
            else:
                if hasattr(chunk.choices[0].delta, "content"):
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    response = response + chunk.choices[0].delta.content
                    response = mistune.html(response)
                return response
    except openai.error.AuthenticationError:
        return "Check Your API Key"
        
    ##Universal (已弃用)
    # #Save conversation
    # History.create(
    #     session_id = SessionID,
    #     UserInput = Userinput,
    #     response = response_out,
    # )

def request_ZhipuAI(APIKEY: str, ModelName:str, RequestURL:str, Userinput: str, historys: list,stream: bool):
    '''
    SessionID 会话在数据库中的ID
    Userinput 用户输入的内容
    stream    是否需要流式传输
    '''
    ##Universal
    #Setup
    messages = []
    response = ""
    
    #Check lib & auto install
    try:
        from zhipuai import ZhipuAI
    except ImportError:
        with ProcessPoolExecutor() as p:
            try:
                p.submit(subprocess.run, "pip install zhipuai")
            except psutil.AccessDenied:
                raise ImportError("No moduel named zhipuai")

    #History
    for r in historys:
        question: Message = {"role": "user", "content": r[0]}
        response_model: Message = {"role": "assistant", "content": r[1]}
        messages.append(question)
        messages.append(response_model)
        
    ##Generated Code
    #Request AI
    try:
        question: Message = {"role": "user", "content": Userinput}
        messages.append(question)
        client = ZhipuAI(APIKEY)
        ZhipuAI.api_base = RequestURL
        for chunk in client.chat.completions.create(
            model=ModelName,
            messages=messages,
            stream=True,
            temperature=0,
        ):
            if stream == True:
                if hasattr(chunk.choices[0].delta, "content"):
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    response = response + chunk.choices[0].delta.content
                    response_out = mistune.html(response)
                    yield response_out
            else:
                if hasattr(chunk.choices[0].delta, "content"):
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    response = response + chunk.choices[0].delta.content
                    response = mistune.html(response)
                return response
    except ZhipuAIError.AuthenticationError:
        return "Check Your API Key"
    


def request_Json(RequestURL: str, Userinput: str, History:list = []):
    response = requests.post(
        url=RequestURL,
        data=json.dumps({"prompt": Userinput, "history": History}),
        headers={"Content-Type": "application/json"},
    )
    response_out = mistune.html(response.json()["history"][0][1])
    return response_out


def uniRequest(API:str, APIKey:str, modelName:str, requestURL:str, userInput: str, historys: list, stream: bool = True):
    if API is None or input is None:
        raise ValueError
    if API == "Json":
        r = request_Json(APIKey, userInput, historys)
        yield r
    if API == "ZhipuAI":
        Model_response = request_ZhipuAI(APIKey, modelName, requestURL, userInput, historys, stream)
        for r in Model_response: 
            yield r
        yield "Check Your API Key"
    if API == "OpenAI":
        Model_response = request_OpenAI(APIKey, modelName, requestURL, userInput, historys, stream)
        for r in Model_response: 
            yield r

    

