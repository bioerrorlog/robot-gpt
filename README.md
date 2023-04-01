# Robot-GPT

[![CI](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml/badge.svg)](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml)

## Usage
Install dependencies:
```sh
pip install -r requirements.txt
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
# Install dev dependencies
pip install -r requirements-dev.txt

# Run camera tests (require a connected camera)
pytest -m 'camera'
```
