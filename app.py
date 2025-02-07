from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, GenerationConfig
from datasets import load_dataset
import random
from tqdm.auto import tqdm
import sys

app = Flask(__name__)

print("Loading dataset...", file=sys.stderr)
huggingface_dataset_name = "knkarthick/dialogsum"
dataset = load_dataset(huggingface_dataset_name)
print("Dataset loaded successfully!", file=sys.stderr)

print("Loading model and tokenizer...", file=sys.stderr)
model_name = "google/flan-t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
print("Model and tokenizer loaded successfully!", file=sys.stderr)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/random-dialogue", methods=["GET"])
def random_dialogue():
    try:
        random_index = random.randint(0, len(dataset['train']) - 1)
        random_dialogue = dataset['train'][random_index]['dialogue']
        return jsonify({"dialogue": random_dialogue})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate-prompt", methods=["POST"])
def generate_prompt():
    try:
        input_data = request.json
        dialogue = input_data.get("dialogue", "")
        prompt_type = input_data.get("prompt_type", "few")

        if prompt_type == "zero":
            prompt = f"Dialogue:\n\n{dialogue}\n\nWhat is going on?"
        elif prompt_type == "one":
            example_dialogue = dataset['test'][6]['dialogue']
            example_summary = dataset['test'][6]['summary']
            prompt = f"""Dialogue:\n\n{example_dialogue}\\nnWhat is going on?\n\n{example_summary}\n\n\nDialogue:\n\n{dialogue}\n\nWhat is going on?"""
        elif prompt_type == "few":
            prompt = ""
            for index in [6, 40, 80, 57]:
                example_dialogue = dataset['test'][index]['dialogue']
                example_summary = dataset['test'][index]['summary']
                prompt += f"""Dialogue:\n\n{example_dialogue}\n\nWhat is going on?\n\n{example_summary}\n\n\n"""
            prompt += f"Dialogue:\n\n{dialogue}\n\nWhat is going on?"
        else:
            return jsonify({"error": "Invalid prompt type."}), 400

        return jsonify({"prompt": prompt})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        input_data = request.json
        prompt = input_data.get("prompt", "")
        do_sample = input_data.get("do_sample", True)
        temperature = input_data.get("temperature", 0.7)
        top_k = input_data.get("top_k", 50)
        top_p = input_data.get("top_p", 0.99)
        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400
        if not isinstance(do_sample, bool):
            return jsonify({"error": "do_sample must be a boolean."}), 400
        if not (0 <= temperature <= 1):
            return jsonify({"error": "Temperature must be between 0 and 1."}), 400
        if not (0 <= top_p <= 1):
            return jsonify({"error": "top_p must be between 0 and 1."}), 400
        if not (top_k >= 0):
            return jsonify({"error": "top_k must be a non-negative integer."}), 400
        if do_sample:
            generation_config = GenerationConfig(
                max_new_tokens=50,
                do_sample=do_sample,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
            )
        else:
            generation_config = GenerationConfig(
                max_new_tokens=50,
                do_sample=do_sample,
            )
        inputs = tokenizer(prompt, return_tensors="pt")
        output = tokenizer.decode(
            model.generate(
                inputs["input_ids"],
                generation_config=generation_config,
            )[0], skip_special_tokens=True
        )
        return jsonify({"summary": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
