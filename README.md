# Grok Insights Bot

## Overview

### Problem
Marketers, startups, and researchers struggle to quickly analyze social media trends on platforms like X, requiring hours of manual data collection and analysis.

### Solution
A Telegram bot that integrates multiple AI-powered APIs (xAI, OpenAI, Hugging Face, uClassify, TextRazor, MonkeyLearn, Watson) to analyze X posts by topic, delivering concise reports on sentiment, keywords, and entities.

### Impact
Provides real-time, actionable insights for marketing campaigns, market research, and trend analysis, saving significant time and effort.

## About the Project
Grok Insights Bot is a Telegram bot that leverages seven AI APIs to analyze X posts and generate detailed reports. Users can select a service, analyze topics, view history, and share results, making it a powerful tool for marketers, bloggers, and data analysts. This project demonstrates my expertise in AI-powered bot development, API integration, database management, and modular code architecture.

## Features
- **Multi-API Text Analysis**: Analyze X posts using seven services (xAI, OpenAI, Hugging Face, uClassify, TextRazor, MonkeyLearn, Watson) for sentiment, keywords, and entities.
- **Interactive UI**: Inline buttons for repeating analysis, sharing results, and viewing history.
- **Database**: SQLite stores analysis history for each user.
- **Localization**: Supports Russian and English languages.
- **Modular Design**: Separate service modules for easy extensibility.

## Installation

### for Linux

1. **Create a project folder**:
   Create a folder named `grok-insights_bot` in your projects directory (e.g., `/home/<YourUsername>/Projects/grok-insights_bot`).
   ```bash
   cd ~/Projects
   mkdir grok-insights_bot
   cd grok-insights_bot
   ```
   Open this folder in VS Code or PyCharm:
   - In VS Code: File → Open Folder → Select `grok-insights_bot`.
   - In PyCharm: File → Open → Select `grok-insights_bot`.

2. **Open a terminal**:
   - In VS Code: Click "Terminal" → "New Terminal" (or press `Ctrl+``).
   - In PyCharm: Click "Terminal" at the bottom of the window.

3. **Install system dependencies**:
   Install tools and libraries needed for Python:
   ```bash
   sudo apt update
   sudo apt install -y build-essential zlib1g-dev libffi-dev libssl-dev libbz2-dev \
   libreadline-dev libsqlite3-dev wget curl llvm libncurses-dev xz-utils tk-dev \
   libxml2-dev libxmlsec1-dev liblzma-dev git
   ```

4. **Install `pyenv`**:
   Install `pyenv` to manage Python versions:
   ```bash
   curl https://pyenv.run | bash
   ```
   Add `pyenv` to your shell configuration:
   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
   echo 'eval "$(pyenv init -)"' >> ~/.bashrc
   echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
   source ~/.bashrc
   ```

5. **Install Python 3.8.10**:
   ```bash
   pyenv install 3.8.10
   ```

6. **Set up a virtual environment**:
   Create and activate a virtual environment:
   ```bash
   pyenv virtualenv 3.8.10 grok-insights-bot
   pyenv local grok-insights-bot
   ```
   Verify Python version:
   ```bash
   python --version
   ```
   Should output `Python 3.8.10`.

7. **Clone the repository**:
   *This step is identical for Linux and Windows.*
   ```bash
   git clone https://github.com/Rostislav62/grok-insights_bot.git .
   ```

8. **Install dependencies**:
   *This step is identical for Linux and Windows.*
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

9. **Configure API keys**:
   *This step is identical for Linux and Windows.*
   Open `config.py` in VS Code or PyCharm and add your API keys:
   ```python
   TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   XAI_API_KEY = "YOUR_XAI_API_KEY"
   OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
   HUGGINGFACE_API_KEY = "YOUR_HUGGINGFACE_API_KEY"
   UCLASSIFY_API_KEY = "YOUR_UCLASSIFY_API_KEY"
   TEXTRAZOR_API_KEY = "YOUR_TEXTRAZOR_API_KEY"
   MONKEYLEARN_API_KEY = "YOUR_MONKEYLEARN_API_KEY"
   WATSON_API_KEY = "YOUR_WATSON_API_KEY"
   ```
   Obtain keys from:
   - Telegram: Create a bot via `@BotFather`.
   - xAI: [x.ai/api](https://x.ai/api).
   - OpenAI: [platform.openai.com](https://platform.openai.com).
   - Hugging Face: [huggingface.co](https://huggingface.co).
   - uClassify: [uclassify.com](https://uclassify.com).
   - TextRazor: [textrazor.com](https://textrazor.com).
   - MonkeyLearn: [monkeylearn.com](https://monkeylearn.com).
   - Watson: [cloud.ibm.com](https://cloud.ibm.com).

10. **Initialize the database**:
    *This step is identical for Linux and Windows.*
    ```bash
    python create_db.py
    ```
    Verify that `insights.db` is created:
    ```bash
    ls insights.db
    ```

11. **Run the bot**:
    *This step is identical for Linux and Windows.*
    ```bash
    python main.py
    ```

12. **Test the bot**:
    *This step is identical for Linux and Windows.*
    - Open Telegram, find your bot (e.g., `@grok_insights_bot`).
    - Send commands: `/start`, `/select_service`, `/analyze AI`.
    - Check responses and verify data in `insights.db`.

### for Windows

1. **Create a project folder**:
   Create a folder named `grok-insights_bot` in your projects directory (e.g., `C:\Users\<YourUsername>\Projects\grok-insights_bot`).
   Open this folder in VS Code or PyCharm:
   - In VS Code: File → Open Folder → Select `grok-insights_bot`.
   - In PyCharm: File → Open → Select `grok-insights_bot`.

2. **Open a terminal**:
   - In VS Code: Click "Terminal" → "New Terminal" (or press `Ctrl+``).
   - In PyCharm: Click "Terminal" at the bottom of the window.

3. **Install Python 3.8**:
   - Download Python 3.8.5 from [python.org](https://www.python.org/downloads/release/python-385/) (select "Windows x86-64 executable installer").
   - Run the installer:
     - Check "Add Python 3.8 to PATH".
     - Select "Customize installation" and ensure "pip" and "Install for all users" are selected.
     - Install to a default path (e.g., `C:\Python38`).
   - Verify in the terminal:
     ```bash
     python --version
     ```
     Should output `Python 3.8.5`.

4. **Install Git**:
   - Download and install Git from [git-scm.com](https://git-scm.com/download/win).
   - During installation, select default options (e.g., "Use Git from the Windows Command Prompt").
   - Verify in the terminal:
     ```bash
     git --version
     ```

5. **Set up a virtual environment**:
   Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
   Your terminal prompt should change to `(venv)`.
   Verify Python version:
   ```bash
   python --version
   ```
   Should output `Python 3.8.5`.

6. **Clone the repository**:
   *This step is identical for Linux and Windows.*
   ```bash
   git clone https://github.com/Rostislav62/grok-insights_bot.git .
   ```

7. **Install dependencies**:
   *This step is identical for Linux and Windows.*
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

8. **Configure API keys**:
   *This step is identical for Linux and Windows.*
   Open `config.py` in VS Code or PyCharm and add your API keys:
   ```python
   TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   XAI_API_KEY = "YOUR_XAI_API_KEY"
   OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
   HUGGINGFACE_API_KEY = "YOUR_HUGGINGFACE_API_KEY"
   UCLASSIFY_API_KEY = "YOUR_UCLASSIFY_API_KEY"
   TEXTRAZOR_API_KEY = "YOUR_TEXTRAZOR_API_KEY"
   MONKEYLEARN_API_KEY = "YOUR_MONKEYLEARN_API_KEY"
   WATSON_API_KEY = "YOUR_WATSON_API_KEY"
   ```
   Obtain keys from:
   - Telegram: Create a bot via `@BotFather`.
   - xAI: [x.ai/api](https://x.ai/api).
   - OpenAI: [platform.openai.com](https://platform.openai.com).
   - Hugging Face: [huggingface.co](https://huggingface.co).
   - uClassify: [uclassify.com](https://uclassify.com).
   - TextRazor: [textrazor.com](https://textrazor.com).
   - MonkeyLearn: [monkeylearn.com](https://monkeylearn.com).
   - Watson: [cloud.ibm.com](https://cloud.ibm.com).

9. **Initialize the database**:
   *This step is identical for Linux and Windows.*
   ```bash
   python create_db.py
   ```
   Verify that `insights.db` is created:
   ```bash
   dir insights.db
   ```

10. **Run the bot**:
    *This step is identical for Linux and Windows.*
    ```bash
    python main.py
    ```

11. **Test the bot**:
    *This step is identical for Linux and Windows.*
    - Open Telegram, find your bot (e.g., `@grok_insights_bot`).
    - Send commands: `/start`, `/select_service`, `/analyze AI`.
    - Check responses and verify data in `insights.db`.


## How to Work with the Bot

### Start the Bot in Telegram
Find the bot by its name (e.g., `@grok_insights_bot`) or start a chat with it.

### Main Commands
- `/start` — Launch the bot and receive a welcome message.
- `/select_service` — Choose an analysis service (xAI, OpenAI, Hugging Face, uClassify, TextRazor, MonkeyLearn, Watson).
- `/analyze <topic>` — Analyze posts by topic (e.g., `/analyze AI`).
- `/history` — View analysis history.
- `/help` — Display the list of commands.

### Example Usage
- Send `/start`.
- Send `/select_service` and choose TextRazor.
- Send `/analyze AI` to receive a report:

Report for topic 'AI' (TextRazor):
Sentiment: Positive
Entities: Artificial intelligence, Machine learning


- Use inline buttons ("Repeat", "Share", "History") for further actions.

### Notes
- **xAI and OpenAI**: Require active credits for full functionality.
- **Hugging Face, uClassify, TextRazor**: Operate in free tiers (~500-1000 requests/day).
- **MonkeyLearn and Watson**: Included as examples but currently inactive (require corporate accounts or credits).
- **Error Handling**: APIs may return "insufficient credits" or similar errors, confirming successful integration.
- Analysis results are stored in `insights.db` for history tracking.

## API Keys
API keys can be obtained from:
- xAI: [x.ai/api](https://x.ai/api)
- OpenAI: [platform.openai.com](https://platform.openai.com)
- Hugging Face: [huggingface.co](https://huggingface.co)
- uClassify: [uclassify.com](https://uclassify.com)
- TextRazor: [textrazor.com](https://textrazor.com)
- MonkeyLearn: [monkeylearn.com](https://monkeylearn.com) (via Medallia)
- Watson: [cloud.ibm.com](https://cloud.ibm.com)

## Project Structure
- `main.py` — Main bot executable.
- `config.py` — Configuration for API keys and services.
- `utils.py` — Utilities for API interactions and SQLite database management.
- `handlers.py` — Command and button handlers.
- `create_db.py` — SQLite database initialization.
- `services/` — API-specific modules:
  - `xai.py`, `openai.py`, `huggingface.py`, `uclassify.py`, `textrazor.py`, `monkeylearn.py`, `watson.py` — Active services.

## Technologies
- **Python 3.8**: Core language.
- **aiogram 2.21**: Telegram Bot API framework.
- **xAI, OpenAI, Hugging Face, uClassify, TextRazor, MonkeyLearn, Watson APIs**: Text analysis.
- **SQLite**: Data storage.
- **aiohttp**: Asynchronous API requests.
- **Git**: Version control.

## Author
Rostislav — AI agent and full-stack developer.  
This project is part of my portfolio, showcasing expertise in AI-powered bot development, multi-API integration, and modular software design.

## License
MIT License
