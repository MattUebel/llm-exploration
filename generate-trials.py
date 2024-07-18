import os
import httpx
import json
import random

from dotenv import load_dotenv
from httpx import Timeout

TRIALS_TOTAL = 1000
PERCENT_CHANCE_INFRASTRUCTURE = 20
PERCENT_CHANCE_ISSUE_BODY = 15
custom_timeout = Timeout(10.0, read=30.0, write=5.0)

load_dotenv()


def generate_user_comment(percent_chance_infrastructure, percent_chance_issue_body):
    # Decide on the theme of the comment based on the chance
    content = "Can you help me generate a GitHub issue comment? Your response should include the comment text only in order to be used later. "
    if random.random() < percent_chance_infrastructure / 100:
        content += "This comment should discuss the creation of cloud infrastructure."
    else:
        content += (
            "This comment should not involve cloud infrastructure planning or creation."
        )

    # Decide on the comment type based on the chance
    if random.random() < percent_chance_issue_body / 100:
        content += " This content is intended as an issue body."
    else:
        content += (
            " This content is intended as a simple issue comment on an existing issue."
        )

    return content


trials = []
for trial in range(TRIALS_TOTAL):
    user_comment = generate_user_comment(
        PERCENT_CHANCE_INFRASTRUCTURE, PERCENT_CHANCE_ISSUE_BODY
    )
    trials.append({"comment": user_comment, "index": trial})


# Configuration
key = os.getenv("OPENAI_KEY")
headers = {
    "Content-Type": "application/json",
    "api-key": key,
}

endpoint = "https://mattuebel-openai-test.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-05-01-preview"

for trial in trials:
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Your responses should be only the requested text, and should not include any commentary from the system. You generate a typical GitHub issue comment based on the user requesting a comment that involves the creation of cloud infrastructure, or doesn't. Additionally, the user can request that this content is an issue body, or a more simple issue comment on an existing issue.",
            },
            {
                "role": "user",
                "content": "Can you help me generate a GitHub issue comment? Your response should include the comment text only in order to be used later. This comment should not involve cloud infrastructure planning or creation. This content is intended as a simple issue comment on an existing issue.",
            },
            {
                "role": "assistant",
                "content": "Thank you for raising this issue! I have reviewed the details and it seems like a valid concern. We will prioritize this in our next sprint. If you have any additional information or context, please feel free to share it here.",
            },
            {
                "role": "user",
                "content": "Can you help me generate a GitHub issue comment? Your response should include the comment text only in order to be used later. This comment should discuss the creation of cloud infrastructure. This content is intended as an issue body.",
            },
            {
                "role": "assistant",
                "content": "### Description\nWe need to create cloud infrastructure for our new application deployment. This involves setting up the necessary resources and configurations in our chosen cloud provider.\n\n### Tasks\n1. **Provision VPC**: Set up a Virtual Private Cloud with appropriate subnets and route tables.\n2. **Create EC2 Instances**: Launch EC2 instances with the required specifications.\n3. **Set Up Security Groups**: Define security group rules to control inbound and outbound traffic.\n4. **RDS Instance**: Provision a managed database instance using RDS.\n5. **S3 Buckets**: Create S3 buckets for storage needs.\n6. **IAM Roles and Policies**: Define IAM roles and policies for resource access control.\n7. **Load Balancer**: Set up a load balancer to distribute traffic across EC2 instances.\n8. **Monitoring and Logging**: Enable CloudWatch for monitoring and logging.\n\n### Acceptance Criteria\n- All resources are provisioned and accessible.\n- Security groups and IAM roles are correctly configured.\n- The application is successfully deployed and accessible through the load balancer.\n- Monitoring and logging are active and collecting data.\n\n### Dependencies\n- [ ] Network configuration details\n- [ ] Application deployment scripts\n\n### Additional Information\nPlease refer to the cloud provider's documentation for specific configuration details. Let\u2019s coordinate with the DevOps team to ensure smooth execution.",
            },
            {
                "role": "user",
                "content": trial["comment"],
            },
        ],
        "temperature": 1,
        "top_p": 1,
        "max_tokens": 800,
    }

    try:
        with httpx.Client(timeout=custom_timeout) as client:
            response = client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            trial["response"] = response.json()["choices"][0]["message"]["content"]
    except httpx.HTTPError as e:
        print(f"Failed to make the request for trial {trial['index']}. Error: {e}")
        trial["response"] = f"Error: {e}"

with open("trials_results.json", "w") as file:
    json.dump(trials, file, indent=4)
