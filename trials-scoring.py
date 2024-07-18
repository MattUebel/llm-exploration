import json
import os
import re

with open("trials_results.json") as file:
    trials = json.load(file)

with open("inference_results.json") as file:
    inference_results = json.load(file)

scoring = []
for trial, inference in zip(trials, inference_results):
    regex = "This comment should not involve cloud infrastructure planning or creation."
    if re.search(regex, trial["comment"]) and inference["response"] == "no":
        score = 1
    elif not re.search(regex, trial["comment"]) and inference["response"] == "yes":
        score = 1
    else:
        print(f"Trial {trial['index']} failed to match the expected response")
        score = -1
    scoring.append({"index": trial["index"], "score": score})

# save the scoring object to a file
with open("scoring.json", "w") as file:
    json.dump(scoring, file, indent=4)
