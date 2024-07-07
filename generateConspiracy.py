import json
import re

from mlx_lm import generate, load


TITLE = "<|begin_of_text|><|start_header_id|>title<|end_header_id|>"
BODY = "<|start_header_id|>body<|end_header_id|>"


def generate_system_prompt(title):
    return f"{TITLE}\n\n{title}<|eot_id|>\n"


def generate_prompt(title):
    prompt = ""
    prompt += generate_system_prompt(title)
    prompt += BODY

    return prompt


def response_to_dict(title, body):
    return {"title": title, "body": body}


def filter_non_standard_characters(text):
    pattern = re.compile(r'[^\w\s.,:;!?\'"@#%&*()\-+=/\\[\]{}<>|`~^]', re.UNICODE)
    cleaned_string = pattern.sub("", text)

    return cleaned_string


class ConspiracyGenerator:
    def __init__(self, model, adapter_path, filepath):
        self.model, self.tokenizer = load(model, adapter_path=adapter_path)
        self.script = []
        self.filepath = filepath

    def generate_theory(self, conspiracy_title, max_tokens=500, temp=0.3):
        response = generate(
            self.model,
            self.tokenizer,
            generate_prompt(conspiracy_title),
            max_tokens,
            verbose=True,
            temp=temp,
            repetition_penalty=1.2,
            repetition_context_size=100,
        )
        filtered_response = filter_non_standard_characters(response)
        theory_dict = response_to_dict(conspiracy_title, filtered_response)
        if theory_dict:
            self.script.append(theory_dict)
            self.write_theory_to_file(theory_dict)
        else:
            print(
                "Error: Could not convert the following response to a theory_dict object:"
            )
            print("---------")
            print(filtered_response)

    # theory = {"title": <title>, "body": <body>}
    def write_theory_to_file(self, theory):
        with open(self.filepath, "a+") as f:
            json.dump(theory, f)
            f.write("\n")


if __name__ == "__main__":
    generator = ConspiracyGenerator(
        "/Users/personal/Desktop/SouthParkDataset/meta-llama/Meta-Llama-3-8B-Instruct",
        "adapters",
        "theories.jsonl",
    )
    title = "Michael Jackson is not the only one doing weird things with children in his theme park"
    for _ in range(5):
        generator.generate_theory(title)
