import json
from typing import List

import openai
import tiktoken

from db.models.dataset import Dataset
from db.queries.dataset_queries import searchDatasetsByEmbedding
from embedding.embedding import embed

# Hacky approach for hackathon: Have to restart API for each new conversation
# TODO: Use a good tool for this stuff like langchain
messageSent = False

firstSystemPrompt = "Please parse the following message, identify  the research topics mentioned in the message, and return only the research topics as a JSON-formatted list of strings. The list should be the top level element, not in any enclosing object."

history = []


def handleMessage(db, userMessage):
    global messageSent

    if not messageSent:
        messageSent = True
        topicList = sendTopicParsingMessage(userMessage)

        datasets = []
        for topic in topicList:
            datasets.append(searchDatasetsByEmbedding(db, embed(topic)))

        return sendDataAnalysisPrompt(datasets)
    else:
        return sendFollowUpPrompt(userMessage)


def sendTopicParsingMessage(userMessage):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{
        "role": "system",
        "content": firstSystemPrompt
    }, {
        "role": "user",
        "content": userMessage
    }])

    return json.loads(completion.choices[0].message.content)


def sendDataAnalysisPrompt(datasets: List[Dataset]):
    prompt = f"Here is information about 2 datasets:\n\n"

    datasetInfo = ""

    for i, dataset in enumerate(datasets):
        datasetInfo += getDatasetDescription(dataset, i)

    prompt += datasetInfo
    prompt += "How can I join these datasets? How might they be related?"

    message = [{
        "role": "user",
        "content": prompt
    }]

    history.append(message[0])

    completion = openai.ChatCompletion.create(
        model="gpt-4", messages=message)

    completionText = completion.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": completionText
    })

    return "Here are some datasets on the topics you expressed interest in:\n\n" + datasetInfo + completionText


def sendFollowUpPrompt(message):
    history.append({
        "role": "user",
        "content": message
    })

    completion = openai.ChatCompletion.create(
        model="gpt-4", messages=history)

    completionText = completion.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": completionText
    })

    return completionText


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def getDatasetDescription(dataset: Dataset, i: int):
    return f"Dataset {i} title: {dataset.title}\n\n" + \
        f"Dataset {i} description: {dataset.description}\n\n" + \
        f"Dataset {i} sample data: {dataset.sampleData}\n\n"
