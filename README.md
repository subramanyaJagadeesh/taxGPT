# TaxGPT

This project is a **tax assistant chatbot** that uses **LLaMA GPT models** to answer U.S. tax-related questions in a user-friendly chat interface. The chat history is saved locally in an **SQLite database** to allow easy retrieval of previous conversations and using that information as context window for further queries. This chatbot is designed to act as a tax accountant, providing responses in HTML format for display purposes.

## Features

- **Chatbot for U.S. Tax-related Queries**: The bot uses the LLaMA GPT model to respond to U.S. tax-related questions.
- **SQLite Database Integration**: Stores chat prompts and responses, allowing users to query historical chats.
- **FastAPI Backend**: Provides REST API endpoints to send/receive chat data and store responses.
- **UI with Recent Chats Sidebar**: Uses Vanilla JS, HTML5, CSS and Bootstramp. Includes a user interface for interacting with the bot and accessing previous chat sessions.
- **CORS Middleware**: Allows API to be accessed from various origins, enabling cross-origin requests.

## Tech Stack

- **Backend**: 
  - [FastAPI](https://fastapi.tiangolo.com/)
  - **SQLite** for local database integration
  - [Ollama API](https://ollama.com/) for interacting with the LLaMA GPT model
- **Frontend**: Bootstrap for UI elements
- **Languages**: Python

## Prerequisites

Ensure you have the following installed:

- **Python 3.8+**
- **SQLite** (comes pre-installed with Python)
- **Ollama** for running the LLaMA model. You need to install and run **Ollama** on your local machine before using the chatbot.
  
### Installing and Running Ollama

- Download and install Ollama from their [official website](https://ollama.com/).
- Once installed, start the Ollama server by running:
  ```bash
  ollama start

## Installation & Running

```bash
git clone https://github.com/your-repo/deloitte-auditor-chat.git
cd deloitte-auditor-chat

pipenv install
pipenv shell

pip install -r requirements.txt
```
### To run the fast API
```bash
fastapi dev taxgpt.py
```

### Open the UI by clicking on the chat_ui.html

## Licenses
- Licensed under the MIT License.

