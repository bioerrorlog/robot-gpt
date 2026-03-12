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

# Run GPT API tests (Warning: The GPT API will be actually called. The API Key is required.)
pytest -s -m 'gpt'

# Run servo moter tests (require connected servo motors)
pytest -m 'servo'

# Run the all tests
pytest -m ''
```

## Blog posts

- [Making LLM the Brain of a Robot - Part 1: Combining a Camera/Servo Motor with GPT - BioErrorLog Tech Blog](https://en.bioerrorlog.work/entry/robot-gpt-prototype)
- [Combining GPT-4 Vision with Raspberry Pi | Making GPT the Brain of a Robot, Part 2 - BioErrorLog Tech Blog](https://en.bioerrorlog.work/entry/robot-gpt-4-vision)
