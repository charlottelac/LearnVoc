This is a Streamlit web app that helps students build their vocabulary in a fun and interactive way.
The teacher enters a word, and the app uses a Large Language Model (LLM) to generate synonyms along with a few distractors. The user must then guess which words are true synonyms.

## Features
- The teacher enters a word
- "Play" button inquires the Mistral LLM that returns 3 real synonyms
- 2 distractors are added to make the game fun and challenging
- "Check" button provides a feedback
- “Next word” button resets the game loop

## Web app 
https://charlottelac-learnvoc-streamlit-app-9doort.streamlit.app/

## Tech Stack
- Streamlit for web app deployement
- LangChain for prompt management
- Mistral API for generating synonyms via LLM

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/charlottelac/LearnVoc.git
cd LearnVoc
```

### 2. Install Dependencies
Make sure you have **Python >= 2.9** installed. Then, install required packages:
```bash
pip install -r requirements.txt
```

The app requires the following libraries:
```bash
streamlit
langchain
langchain-mistralai
```

### 3. Add your Mistral API key
If you want to run the app locally, create a .streamlit/secrets.toml file:
```toml
api_key = "your-mistral-api-key"
```

### 4. Run the Streamlit App
```bash
streamlit run streamlit_app.py
```

### 5. Deploying on Streamlit Cloud
	1.	Push your app to GitHub.
	2.	Go to Streamlit Cloud.
	3.	Connect your repo and click “Deploy”.
	4.	In “Secrets”, paste:

```toml
api_key = "your-mistral-api-key"
```

## License 
This project is open-source and available under the **MIT License**.

---
🔗 **Developed by Charlotte L**