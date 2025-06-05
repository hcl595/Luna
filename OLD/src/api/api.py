from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import StreamingResponse
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder

#Original
from Luna.extractor import write_pyFile
from Luna.kit import uniRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "200"}

@app.post("/request_models_stream")
async def request_models_stream(
    InputAPIType:str = Form(),
    InputAPIKey:str = Form(),
    InputModelName:str = Form(),
    InputUrl:str = Form(),
    InputQuestion:str = Form(),
    InputHistorys:str = Form()
    ):
    if not InputAPIType or not InputAPIKey or not InputUrl or not InputQuestion:
        raise HTTPException(status_code=400, detail="Missing userinput or modelinput")
    if not InputHistorys:
        InputHistorys = []
    else:
        InputHistorys = jsonable_encoder(InputHistorys)
    async def stream():
        async for response in uniRequest(
            API=InputAPIType,
            APIKey=InputAPIKey,
            modelName=InputModelName,
            requestURL=InputUrl,
            userInput=InputQuestion,
            historys=InputHistorys,
            stream=True):
            yield response
    return StreamingResponse(stream(), media_type="text/plain")