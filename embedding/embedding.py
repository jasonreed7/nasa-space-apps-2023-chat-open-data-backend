import os

import requests
from retry import retry

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = os.getenv("HF_TOKEN")

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

filesToEmbed = ["dataset-info/air-quality.txt"]


@retry(tries=3, delay=10)
def embed(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts})
    result = response.json()
    if isinstance(result, list):
        return result
    elif list(result.keys())[0] == "error":
        raise RuntimeError(
            "The model is currently loading, please re-run the query."
        )


def embedFiles():
    texts = []
    for fileName in filesToEmbed:
        file = open(fileName, "r")
        texts.append(file.read())
    resp = embed(texts)
    print(resp)


if __name__ == "__main__":
    embedFiles()
