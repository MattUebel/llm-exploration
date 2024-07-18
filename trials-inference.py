import os
import httpx
import json
import random

from dotenv import load_dotenv
from httpx import Timeout

custom_timeout = Timeout(10.0, read=30.0, write=5.0)

load_dotenv()

# Configuration
key = os.getenv("OPENAI_KEY")
headers = {
    "Content-Type": "application/json",
    "api-key": key,
}

endpoint = "https://mattuebel-openai-test.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-05-01-preview"

with open("trials_results.json") as file:
    trials = json.load(file)

for trial in trials:
    trial["comment"] = trial["response"]
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You analyze github issue comments to determine if they seems to involve the modification (creation or deletion) of cloud infrastructure. The user will enter the text of an issue body or comment, your response should be a single word: 'yes' or 'no'.",
            },
            {
                "role": "user",
                "content": "Thank you for raising this issue! I have reviewed the details and it seems like a valid concern. We will prioritize this in our next sprint. If you have any additional information or context, please feel free to share it here.",
            },
            {
                "role": "assistant",
                "content": "no",
            },
            {
                "role": "user",
                "content": "I agree with the points raised in this issue. For the creation of the cloud infrastructure, we should consider using Terraform to manage the resources and ensure that we have a well-defined infrastructure as code. Additionally, leveraging AWS CloudFormation templates could help streamline the deployment process. Let's discuss the specifics in our next meeting.",
            },
            {
                "role": "assistant",
                "content": "yes",
            },
            {
                "role": "user",
                "content": trial["comment"],
            },
        ],
        "temperature": 0,
        "top_p": 0,
        "max_tokens": 800,
    }

    try:
        with httpx.Client(timeout=custom_timeout) as client:
            response = client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            trial["response"] = response.json()["choices"][0]["message"]["content"]
    except httpx.HTTPError as e:
        print(f"Failed to make the request for inference {trial['index']}. Error: {e}")
        trial["response"] = f"Error: {e}"

with open("inference_results.json", "w") as file:
    json.dump(trials, file, indent=4)
