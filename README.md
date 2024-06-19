# llm-deepseek

[![PyPI](https://img.shields.io/pypi/v/llm-deepseek.svg)](https://pypi.org/project/llm-deepseek/)
[![Changelog](https://img.shields.io/github/v/release/abrasumente233/llm-deepseek?include_prereleases&label=changelog)](https://github.com/abrasumente233/llm-deepseek/releases)
[![Tests](https://github.com/abrasumente233/llm-deepseek/actions/workflows/test.yml/badge.svg)](https://github.com/abrasumente233/llm-deepseek/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/abrasumente233/llm-deepseek/blob/main/LICENSE)

Access [deepseek.com](https://deepseek.com/) models via API

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-deepseek
```
## Usage

Obtain a [DeepSeek API key](https://platform.deepseek.com/api_keys) and save it like this:

```bash
llm keys set deepseek
# <Paste key here>
```
Run `llm models` to get a list of models.

Run prompts like this:
```bash
llm -m deepseek-chat 'five great names for a pet ocelot'
llm -m deepseek-coder 'how to reverse a linked list in python'
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-deepseek
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest
```
