# Robot-GPT

[![CI](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml/badge.svg)](https://github.com/bioerrorlog/robot-gpt/actions/workflows/ci.yml)

## Usage
Install dependencies:
```sh
# Rust compiler required
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Dev packages
sudo apt install libffi-dev

# Python libraries
poetry install
```

Run the script:
```sh
# Set your OpenAI API key
export OPENAI_API_KEY=your_openai_api_key

# Run the script
poetry run python -m robot_gpt.main
```

## Running tests
```sh
# Run camera tests (require a connected camera)
poetry run pytest -m 'camera'
```
