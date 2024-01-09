from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import typing
import httpx
import json
from transformers import AutoTokenizer
import tiktoken
import os

model_env_var = os.getenv("MODEL", "mistralai/Mistral-7B-Instruct-v0.1")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")

token_data = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
}

tokenizer_oai = tiktoken.get_encoding("cl100k_base")
tokenizer_local = AutoTokenizer.from_pretrained(model_env_var)

@app.post("/v1/chat/completions")
async def chat_completion(request: Request):
    body = await request.json()

    # Process logit_bias
    logit_bias = body.get("logit_bias", {})
    logit_bias_reimplement = {}
    for key, value in logit_bias.items():
        ids = tokenizer_local.convert_tokens_to_ids(tokenizer_local.tokenize(tokenizer_oai.decode([int(key)])))
        for i in ids:
            logit_bias_reimplement[str(i)] = value
    body["logit_bias"] = logit_bias_reimplement
    body["model"] = model_env_var

    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post("http://localhost:2242/v1/chat/completions", json=body)
        response_data = response.json()

        usage = response_data.get("usage", {})
        token_data["prompt_tokens"] += usage.get("prompt_tokens", 0)
        token_data["completion_tokens"] += usage.get("completion_tokens", 0)

        return response_data

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Pass the model ID and token data to the HTML template
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "model_id": model_env_var, "token_data": token_data}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
