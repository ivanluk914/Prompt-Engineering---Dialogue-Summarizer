# Prompt-Engineering---Dialogue-Summarizer

**Dialogue Summarizer** is a web application designed to summarize dialogues using natural language processing (NLP) capabilities provided by a pre-trained transformer model. This project utilizes the **Hugging Face Transformers** library and a small subset of the Dialogue Summarization dataset from Hugging Face to create concise summaries of conversations.

## Features

- Enter a custom dialogue and summarize it using an NLP model.
- Use prompt engineering techniques such as:
  - Zero-shot prompts
  - One-shot prompts
  - Few-shot prompts
- Random dialogue generation from the dataset for experimentation.
- Configurable sampling parameters (temperature, top-k, top-p) for customizable generation.
- Use of **Flask** web framework for the backend API and **Google-FLAN-T5** as the base transformer model.

## Tech Stack

### Frontend
- HTML, JavaScript, and CSS
- **Bootstrap** for styling

### Backend
- **Flask** (Python 3.9)
- **Hugging Face Transformers**
- **PyTorch**

### Deployment
- Dockerized application for seamless deployment with **Gunicorn** as the production WSGI server.

---

## Project Structure

```plaintext
.
├── app.py                 # Main Flask server application
├── templates/             # Frontend HTML directory
    ├── index.html
├── Dockerfile             # Docker container definition
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## Installation and Usage

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

### 2. Build and Run Locally

#### Set up a Virtual Environment (Optional)
It is recommended to use a virtual environment for Python dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Run Locally

```bash
python app.py
```

Visit the web application on: `http://127.0.0.1:5001`

---

### 3. Run with Docker

#### Build Docker Image
```bash
docker build -t dialogue-summarizer .
```

#### Run Docker Container
```bash
docker run -p 5001:5001 dialogue-summarizer
```

Visit the web application on: `http://127.0.0.1:5001`

---

## Endpoints

### `/`
Renders the web application's frontend interface.

### `/random-dialogue`
GET endpoint to retrieve a random dialogue from the dataset.

### `/generate-prompt`
POST endpoint to generate a prompt using the dialogue and the specified prompting type.

Payload (JSON):
```json
{
  "dialogue": "Your dialogue here...",
  "prompt_type": "few"  // Options: "few", "zero", "one"
}
```

### `/summarize`
POST endpoint to summarize the dialogue using the specified parameters.

Payload (JSON):
```json
{
  "prompt": "Generated dialogue prompt...",
  "do_sample": true,
  "temperature": 0.7,
  "top_k": 50,
  "top_p": 0.99
}
```

---

## Requirements

- Python 3.9+
- Docker (optional, for containerized deployment)

### Python Libraries

The following are the main libraries required for this project (see `requirements.txt` for all dependencies):

- `datasets`
- `transformers`
- `flask`
- `torch`
- `gunicorn`

---

## How it Works

1. **Frontend**  
   Users can enter a dialogue, generate a random one, or input their custom text for summarization. Configure parameters or prompt types for fine-tuning the summarization behavior.

2. **Backend**  
   Flask provides APIs for interaction, while the backend integrates with a pre-trained **FLAN-T5** model to process prompts and generate summarization outputs.

3. **Deployment**  
   The project is containerized using Docker for deployment, with **Gunicorn** as the production-ready application server.

---

## Contributing

Contributions are welcome! Feel free to create pull requests or open issues on the GitHub repository.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Special thanks to:

- [Hugging Face](https://huggingface.co/) for their amazing models and dataset library.
- The [DialogSum Dataset](https://huggingface.co/datasets/knkarthick/dialogsum) authors.
- The [FLAN-T5 Model](https://huggingface.co/google/flan-t5-base) by Google.
