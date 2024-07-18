# GitHub Issue Comment Generation Project

This project consists of two main scripts, `generate-trials.py` and `trials-inference.py`, which work together to generate and infer GitHub issue comments related to cloud infrastructure. The project uses OpenAI's GPT models to generate comments based on specified criteria and then infers whether these comments involve the creation or deletion of cloud infrastructure.

## Overview

- `generate-trials.py`: Generates a set of trial comments based on specified criteria, such as the percentage chance of the comment discussing cloud infrastructure and whether it is intended as an issue body or a simple comment.
- `trials-inference.py`: Takes the generated comments and uses an OpenAI model to infer whether each comment involves cloud infrastructure creation or deletion.

## Prerequisites

- Python 3.12
- Pipenv for managing project dependencies

## Setup

1. **Clone the repository**:
   Clone this repository to your local machine using `git clone`.

2. **Install dependencies**:
   Navigate to the project directory and run `pipenv install` to create a virtual environment and install the required dependencies listed in the `Pipfile`.

3. **Environment Variables**:
   Create a `.env` file in the root of the project directory. Add your OpenAI API key as follows:

```
OPENAI_KEY=your_openai_api_key_here
```

## Usage

1. **Generating Trials**:
- Run `pipenv run python generate-trials.py` to generate a set of trial comments. This script will create a JSON file named `trials_results.json` containing the generated comments and their details.

2. **Running Inference**:
- After generating the trials, run `pipenv run python trials-inference.py` to infer whether the comments involve cloud infrastructure. This script reads the `trials_results.json` file, performs inference using the OpenAI model, and outputs the results to `inference_results.json`.

## Configuration

- You can adjust the number of trials, percentage chances for infrastructure-related comments, and issue body comments by modifying the constants at the beginning of `generate-trials.py`.
- The endpoint and headers for the OpenAI API request are configured in both scripts. Ensure your API key and endpoint URL are correctly set in the `.env` file and the scripts.

## Note

- Ensure you have sufficient OpenAI API credits as both scripts make requests to the OpenAI API.
- The scripts are configured to use a specific OpenAI model endpoint. If you wish to use a different model or endpoint, update the `endpoint` variable in both scripts accordingly.