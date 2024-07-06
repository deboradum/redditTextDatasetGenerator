import csv
import json
import os
import random


OUTPUT_PATH = "conspiracySubmissionsData"


class Submission:
    upvotes = 0
    date = 1
    title = 2
    user = 3
    url = 4
    body = 5


SYSTEM = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>"
USER = "<|start_header_id|>user<|end_header_id|>"
ASSISTENT = "<|start_header_id|>assistant<|end_header_id|>"


def generate_prompt(title, body):
    return f"<|start_header_id|>title<|end_header_id|>{title}<|eot_id|>\n<|start_header_id|>body<|end_header_id|>{body}<|eot_id|>\n"


def is_url(text):
    return "http" in text


def is_removed(text):
    return text == "[removed]" or text == "[deleted]" or text.strip() == ""


def write_to_file(title, body):
    num = random.random()
    if num < 0.7:
        with open(f"{OUTPUT_PATH}/train.jsonl", "a+") as output_f:
            output_f.write(json.dumps({"text": generate_prompt(title, body)}) + "\n")
    elif num < 0.85:
        with open(f"{OUTPUT_PATH}/test.jsonl", "a+") as output_f:
            output_f.write(json.dumps({"text": generate_prompt(title, body)}) + "\n")
    else:
        with open(f"{OUTPUT_PATH}/valid.jsonl", "a+") as output_f:
            output_f.write(json.dumps({"text": generate_prompt(title, body)}) + "\n")


def parse_submissions(filepath):
    with open(filepath, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        i = 0
        for row in csv_reader:
            title = row[Submission.title]
            body = row[Submission.body]
            if not is_url(body) and not is_url(body) and not is_removed(body):
                write_to_file(title, body)
                i += 1
                if i % 10000 == 0:
                    print(f"Parsed {i} submissions")


if __name__ == "__main__":
    filepath = "dumpsParsed/conspiracy_submissions.csv"
    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    if "submissions" in filepath:
        parse_submissions(filepath)
