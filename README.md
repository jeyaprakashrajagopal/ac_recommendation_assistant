# Project Title: 
LLM powered AC Recommendation Assistant.
## Description:
It is a very time-consuming and difficult process to select an air conditioner by going through the specifications of all air conditioners manually. In addition, going through all the specifications would be challenging for someone who has never had an air conditioner in their home. So, it would be a daunting task for many people to make the decision. This AC recommendation assistant is the solution to this underlying problem.

## Getting Started
### Dependencies
* This project has been developed in VSCode with an uv project manager tool. It also includes dependencies such as `Flask`, `pandas`, `dependency_injector`, `openai`, `python-dotenv`, `tenacity` and `pytest`. All the dependencies can be found in `pyproject.toml` file in the main directory.

### Execution
This section provides the setup and execution
* Navigate to the main project directory.
* Create .env file and add the following with your own secret key instead of `sk_`
```
OPENAI_API_KEY=sk_
```
* If `uv` project manager is not installed in your pc, please run the following command in terminal
```
pip install uv
```
* To satisfy and sync all the project requirements, please run the following command in terminal
```
uv sync
```
* Now, it is possible to execute the program and launch the application by entering the following command in terminal
```
uv run main.py
```
* It is possible to run the unit tests with the following command
```
python -m pytest
```
#### Entry Point
The application starts from **`main.py`**, which initializes and executes the flash app.
### Execution Flow

1. **`main.py`**
    - Starts the Flask app.
    - Loads the configuration from `src/model/openai_config.py`.
    - Starts executing the pipeline.
2. **Dependency Injection `src/di`**
    - Wires together models, pipeline, and stages.
    - Ensures modules are loosely coupled and testable.
3. **Pipeline**
    - Orchestrates the complete workflow of the project.
    - Makes use of different **stages** from `src/stages` to process the data.
4. **Models (`src/model`)**
    - Provides interfaces and implementation of OpenAI models such as moderation check, chat completion API's.
        - This provides abstraction hence it supports the integration of different models.
5. **Prompts (`src/prompts`)**
    - Stores all the prompts as markdown (md) files used by the pipeline for all the stages.
6. **Utilities (`src/utils`)**
    - Common helper functions used in the project.

### Project structure
config/ # Global settings (file paths)
data/static # static datasets
src/
    di/# Dependency injection modules
    model/ # model interfaces & implementation
    pipeline/ # Orchestrator
    prompts/ # Prompts as markdown files
    stages/ # Implementation of all stages in pipeline
    utils/ # Shared utilities
static/ # Static image files
static/css/ # Stylesheets
templates/ # HTML template files
tests/ # Unit tests
tests/stages # Unit tests specific for all stages of the pipeline
main.py # Application entry point
pyproject.toml # Project metadata and the dependencies
.env # To keep all the secret keys in environment for safety purposes, openai key is stored in this project
.gitignore # Files to be ignored during git push