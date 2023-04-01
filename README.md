# Robot-GPT

[![CI](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml/badge.svg)](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml)

## Usage
Install dependencies:
```sh
poetry install
```

Run the script:
```sh
# Set your OpenAI API key
export OPENAI_API_KEY=your_openai_api_key

# Run the script
python robot_gpt/main.py
```

## Running tests
```sh
# Run camera tests (require a connected camera)
pytest -m 'camera'
```
