from openai import OpenAI
import os
import json

rag_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_conf = os.path.join(rag_dir, "conf", "model.json")

model_url = None
client = None


def init(tool: str) -> str:
    if not os.path.exists(model_conf):
        raise FileNotFoundError(f"Model configuration file not found: {model_conf}")

    with open(model_conf, "r", encoding="utf-8") as f:
        config = json.load(f)

    if tool not in config:
        raise ValueError(f"Tool config not found: {tool}")

    model_url = config[tool].get("model_url")

    if not model_url:
        raise ValueError(f"Model URL not found for tool: {tool}")

    return model_url


def get_model_url(tool: str) -> str:
    return init(tool)


def gen_openai_client(tool: str) -> OpenAI:
    global model_url, client

    model_url = get_model_url(tool)

    client = OpenAI(
        base_url=model_url,
        api_key="EMPTY"
    )

    return client


def get_openai_client() -> OpenAI:
    global client

    if client is None:
        raise ValueError("OpenAI client is not initialized. Call gen_openai_client(tool) first.")

    return client

def send_request_to_openai(prompt: str, tool: str) -> dict:
    gen_openai_client(tool)
    client = get_openai_client()
    response = client.responses.create(
        model="qwen3.6:35b",
        input=prompt
    )
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    return {"text": content.text}
    return {"text": ""}
