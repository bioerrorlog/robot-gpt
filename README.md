# Robot-GPT

[![CI](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml/badge.svg)](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml)

## Usage
Install dependencies:
```sh
pip install -r requirements.txt
```

Download the pre-trained model:
```sh
curl -L -o ./models/tiny-yolov3.pt https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/tiny-yolov3.pt
```

Run the script:
```sh
# Set your OpenAI API key
export OPENAI_API_KEY="your_openai_api_key"

# Run the script
python -m robot_gpt.main
```

## Running tests
```sh
# Install dev dependencies
pip install -r requirements-dev.txt

# Run camera tests (require a connected camera)
pytest -m 'camera'

# Run image recognition tests (require downloading the pre-trained model)
pytest -m 'recognize'

# Run ChatGPT API tests (Warning: The ChatGPT API will be actually called. The API Key is required.)
pytest -s -m 'chatgpt'
```
