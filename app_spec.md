# Gemini LangGraph Multi-Turn Agent App Specification

## Overview

This document describes a simple Python application that uses Gemini via the langchain-google-genai package and LangGraph for a multi-turn agent system.

The application contains:
- a Gemini model loader that reads the API key from the environment or prompts the user
- a tool library for career path recommendations and learning resources
- two agents: a career advisor and an education advisor
- a multi-turn controller that transfers between advisors
- a simulator with both sample and interactive modes

The spec contains no source code, only precise descriptions of required files, functions, and behavior.

## Dependencies

The application depends on:
- a Gemini-compatible LangChain integration package
- LangGraph
- langchain-core
- typing-extensions
- getpass (standard library)
- os, uuid, sys (standard library)

## Environment

The app uses a single environment variable:
- `GOOGLE_API_KEY`

If `GOOGLE_API_KEY` is not already set, the app should prompt the user for it during startup.

## File structure

The project should contain these files:
- `requirements.txt`
- `llm.py`
- `agentTools.py`
- `agent_definitions.py`
- `AgentTaskWrapper.py`
- `agentMultiTurnController.py`
- `simulator.py`
- `agents.py`
- `langgraph_multi_turn_agent.py`

## File specifications

### `requirements.txt`

Describe the external Python packages needed to run the app. It should include the Gemini LangChain integration package, LangGraph, langchain-core, and typing-extensions.

### `llm.py`

Purpose:
- create and configure the Gemini chat model
- resolve the API key and model name

Required behavior:
- define a function named `get_model` that accepts optional arguments `model_name` and `api_key`
- if `api_key` is not passed, read `GOOGLE_API_KEY` from the environment
- if the env var is not set, print a message and prompt the user via a secure terminal prompt for the API key
- if the user enters a key, store it in the current process environment for later use
- once the API key is resolved, choose a model name defaulting to `gemini-3.6-flash` unless overridden by `GEMINI_MODEL`
- return a Gemini-compatible chat model object created with the resolved model and API key

### `agentTools.py`

Purpose:
- define reusable tools for the agents

Tools to define:
- `get_career_paths`: returns a career suggestion string chosen from data science, product management, or cybersecurity
- `get_learning_resources`: accepts a career string and returns a list of resources appropriate for that career
- `transfer_to_education_advisor`: returns a direct transfer message to signal switching to the education advisor
- `transfer_to_career_advisor`: returns a direct transfer message to signal switching back to the career advisor

Implementation notes:
- use the LangChain tool decorator style to register each function as a tool
- `transfer_to_education_advisor` and `transfer_to_career_advisor` should be direct return tools

### `agent_definitions.py`

Purpose:
- instantiate the two advisor agents with their prompts and tools

Required behavior:
- import the Gemini model loader from `llm.py`
- import the tools from `agentTools.py`
- use the LangGraph `create_react_agent` factory with the resolved model
- create `career_advisor` using the career tools and a career advisor prompt
- create `education_advisor` using the education tools and an education advisor prompt
- export both advisor objects

Prompt requirements:
- career advisor prompt should instruct the model to act as a career expert, transfer to the education advisor when users ask about courses or education, and explain reasoning before transferring
- education advisor prompt should instruct the model to act as an education expert, transfer back to the career advisor if the user changes career preference, and explain reasoning before transferring

### `AgentTaskWrapper.py`

Purpose:
- wrap both advisors as LangGraph tasks that accept message lists

Required behavior:
- define a task function `call_career_advisor(messages)` that invokes the career advisor with the provided messages and returns the resulting message list
- define a task function `call_education_advisor(messages)` that does the same for the education advisor

### `agentMultiTurnController.py`

Purpose:
- manage the multi-turn conversation flow between advisors

Required behavior:
- create a LangGraph entrypoint named `multi_turn_graph`
- use a memory saver to persist conversation state
- accept incoming `messages` and optional `previous` conversation state
- append new messages to prior history using LangGraph message utilities
- begin with the career advisor as the active agent
- run a loop that invokes the active agent task and appends the agent messages to the conversation
- locate the last AI message in the agent output
- if the AI message contains no tool calls, interrupt for user input and append that user message
- if the AI message includes a transfer tool call, switch the active agent accordingly
- support transfer tool names `transfer_to_education_advisor` and `transfer_to_career_advisor`

### `agents.py`

Purpose:
- re-export the two advisor objects for easy imports

Required behavior:
- import `career_advisor` and `education_advisor` from `agent_definitions.py`
- export them in `__all__`

### `simulator.py`

Purpose:
- provide both sample simulation and interactive terminal runner

Required behavior:
- define a helper to extract readable text from nested AI content payloads
- define `run_simulation()` that sends a fixed sequence of inputs through `multi_turn_graph.stream` and prints clean AI responses
- define `run_interactive_chat()` that reads user input from the terminal, sends it to the active advisor, prints clean responses, and handles advisor transfers
- support friendly exit on `exit`, `quit`, or Ctrl+C
- if launched with `--interactive`, run the interactive loop; otherwise run the sample simulation

Text extraction notes:
- handle string content directly
- if content is a list, recursively extract text from each item and join with newlines
- if content is a dictionary, extract `text` or `content` fields

### `langgraph_multi_turn_agent.py`

Purpose:
- prompt for `GOOGLE_API_KEY` when the app starts if it is not already set

Required behavior:
- define a helper that checks the environment for a given variable name
- if the variable is absent, prompt the user with a secure terminal prompt and set it in `os.environ`
- call this helper for `GOOGLE_API_KEY`

## Running the app

Instructions:
- install the required packages
- optionally set `GOOGLE_API_KEY` in the environment
- run `python simulator.py --interactive` to start the chat
- run `python simulator.py` to execute the sample conversation

## Generation guidance

To generate the code base from this specification, create each file exactly as described above.

For each Python file, follow the function names, structural responsibilities, and behavior notes in this document.

The markdown should be sufficient for a code generator to create:
- file names
- import relationships
- function signatures
- prompt text behavior
- environment variable handling
- the multi-turn advisor handoff flow

## Notes

- no code is included in this document
- this is a design-level specification for the application
- if a code generator needs more detail, it should infer the Python equivalents from the described behavior
