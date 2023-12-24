# Robot-GPT

[![CI](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml/badge.svg)](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml)

Robot with GPT as the brain.

## Usage
Install dependencies:
```sh
pip install -r requirements.txt
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

# Run ChatGPT API tests (Warning: The ChatGPT API will be actually called. The API Key is required.)
pytest -s -m 'chatgpt'

# Run servo moter tests (require connected servo motors)
pytest -m 'servo'

# Run the all tests
pytest -m ''
```
