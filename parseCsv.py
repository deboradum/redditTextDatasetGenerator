import csv
import json
import os
import random
import argparse

class Submission:
    upvotes = 0
    date = 1
    title = 2
    user = 3
    url = 4
    body = 5


def is_url(text):
    return "http" in text or "www." in text


def is_removed(text):
    return text == "[removed]" or text == "[deleted]" or text.strip() == ""


def is_reddit_redirect(text):
    return "/r/" in text or "r/" in text


def too_short(text, min_len=10):
    return len(text.split(" ")) < min_len


# In general posts starting with or ending with these words are low quality.
def invalid_title(text):
    if text.lower().startswith(("why", "i", "so", "what", "when", "if", "how")):
        return True
    if text.lower().endswith(("?")):
        return True
    return False


def write_to_file(title, body, output_path):
    os.makedirs(output_path, exist_ok=True)
    num = random.random()
    # 70/15/15 split
    if num < 0.7:
        with open(f"{output_path}/train.jsonl", "a+", encoding="utf-8") as output_f:
            output_f.write(json.dumps({"title": title, "body": body}) + "\n")
    elif num < 0.85:
        with open(f"{output_path}/test.jsonl", "a+", encoding="utf-8") as output_f:
            output_f.write(json.dumps({"title": title, "body": body}) + "\n")
    else:
        with open(f"{output_path}/valid.jsonl", "a+", encoding="utf-8") as output_f:
            output_f.write(json.dumps({"title": title, "body": body}) + "\n")


def parse_submissions(filepath, output_path):
    with open(filepath, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        i = 0
        for row in csv_reader:
            title = row[Submission.title]
            body = row[Submission.body]
            if (
                not is_url(body)  # Exclude url posts
                and not is_removed(body) # Exclude removed posts
                and not is_reddit_redirect(body)  # Exclude redirected posts
                and not too_short(body, min_len=500)  # Exclude posts with short body
                and not too_short(title, min_len=4)  # Exclude posts with short title
                and not invalid_title(title)  # Filtering low quality posts which are questions, etc.
            ):
                write_to_file(title, body, output_path)
                i += 1
        print(f"{i} total posts")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Path to submissions CSV file")
    parser.add_argument("output", help="Output directory for train/test/valid JSONL files")
    args = parser.parse_args()

    filepath = args.filepath
    output_path = args.output
    os.makedirs(output_path, exist_ok=True)

    # Currently only submissions are supported
    parse_submissions(filepath, output_path)
