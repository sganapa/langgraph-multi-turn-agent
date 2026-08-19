# Gemini LLM Access Details

This project uses Google Gemini through LangChain's `ChatGoogleGenerativeAI` wrapper.

## Requirements

Install the Python packages used by the LLM helper:

```powershell
pip install langchain-google-genai
```

If you are using the complete LangGraph application, install its other project dependencies as well.

## API key setup

Create a Gemini API key in Google AI Studio, then provide it through the `GOOGLE_API_KEY` environment variable.

### Windows PowerShell: current terminal only

```powershell
$env:GOOGLE_API_KEY = "your-gemini-api-key"
```

### Windows PowerShell: persistent user variable

```powershell
[Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", "your-gemini-api-key", "User")
```

Restart VS Code or the terminal after setting a persistent variable.

### Command Prompt: current terminal only

```cmd
set GOOGLE_API_KEY=your-gemini-api-key
```

Do not commit API keys to source control or place real keys in this Markdown file.

## Optional model selection

The helper reads the model name from `GEMINI_MODEL`. If it is not set, the current default in `llm.py` is `gemini-3.6-flash`.

PowerShell:

```powershell
$env:GEMINI_MODEL = "gemini-2.5-flash"
```

The model can also be selected directly in Python.

## Use from Python

From a file in this project:

```python
from llm import get_model

model = get_model()
response = model.invoke("Explain LangGraph in one paragraph.")
print(response.content)
```

Use a specific model:

```python
from llm import get_model

model = get_model(model_name="gemini-2.5-flash")
response = model.invoke("Give me three Python learning tips.")
print(response.content)
```

Pass an API key directly when required by an external application. Prefer environment variables for normal local development:

```python
from llm import get_model

model = get_model(
    model_name="gemini-2.5-flash",
    api_key="your-gemini-api-key",
)
```

## Existing project integration

The advisor setup already obtains the configured model through `get_model()`:

```python
from llm import get_model

model = get_model()
```

This model can then be passed to LangGraph or LangChain components such as `create_react_agent`.

## Authentication behavior

`get_model()` resolves credentials in this order:

1. The `api_key` argument, when supplied.
2. The `GOOGLE_API_KEY` environment variable.
3. An interactive prompt for the Gemini API key.

If a key is entered at the prompt, it is stored in the current Python process environment. If no key is supplied, the helper raises a `RuntimeError`.

## Troubleshooting

- `No GOOGLE_API_KEY found in the environment.`: set `GOOGLE_API_KEY`, pass `api_key=...`, or allow the interactive prompt.
- Authentication or permission errors: verify that the key is valid and that the selected Gemini model is available to your account.
- Model errors: set `GEMINI_MODEL` to a model name supported by your Google Gemini account.
- Import errors: activate the intended Python environment and install `langchain-google-genai` there.

## Reusing this helper elsewhere

Copy `llm.py` and this document into the target project, install `langchain-google-genai`, and expose the same environment variables. Then import the helper from the copied module:

```python
from llm import get_model
```

If the module has a different filename or package location, update the import accordingly.
