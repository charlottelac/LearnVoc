import streamlit as st
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
import random
import re

#api_key = os.getenv("MISTRAL_API_KEY")
# API KEY stored in secret file 
#api_key = st.secrets["mistral"]["api_key"]
api_key = st.secrets["api_key"]

# Streamlit app title
st.title("Enrich your vocabulary")

if "choices" not in st.session_state:
    st.session_state.choices = []

if "correct_synonyms" not in st.session_state:
    st.session_state.correct_synonyms = []

if "wrong_words" not in st.session_state:
    st.session_state.wrong_words = []

if "new_round" not in st.session_state:
    st.session_state.new_round = False

if "score" not in st.session_state:
    st.session_state.score = 0

# Input word
st.text_input("Enter a word", key = "word")

# Extract LLM model's answers when format is wrong
def extract_words_in_brackets(text):
    # Use regular expression to find the content within brackets
    match = re.search(r'\(([^)]+)\)', text)
    if match:
        # Split the content by comma and strip any extra whitespace
        words = [word.strip() for word in match.group(1).split(',')]
        return words
    else:
        return None


def load_new_round():
    if not st.session_state.word:
        st.warning("Please enter a word and press Play.")
        return
    # Prompt LLM to ask for synonyms
    system_template = "Give 3 synonyms for this word: {word}, formatted as a comma-separated list (e.g., fast, quick, speedy)."

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template)]
    )

    # Choose the LLM model 
    llm_model = "mistral-large-latest"

    #llm_model = "mistral-small-latest"
    model = init_chat_model(llm_model, model_provider="mistralai", api_key=api_key)

    # Get an answer
    prompt = prompt_template.invoke({"word": st.session_state.word})
    synonyms = model.invoke(prompt)
    synonyms_list = [resp.lower().strip(' ').strip('(').strip(')') for resp in synonyms.content.split(",")]

    # Generate disctractors
    system_template_dist = "Give 2 words that have a different meaning than this list of words: {list_w}, formatted as a comma-separated list such as (fast, quick)."

    prompt_template_dist = ChatPromptTemplate.from_messages(
        [("system", system_template_dist)]
        )

    list_w = synonyms_list + list(st.session_state.word)

    prompt_dist = prompt_template_dist.invoke({"list_w": list_w})

    resp_distractors = model.invoke(prompt_dist)
    distractors = extract_words_in_brackets(resp_distractors.content)

    # Store synonyms and distractors
    words_choice = synonyms_list + distractors
    random.shuffle(words_choice)
    st.session_state.choices = words_choice
    st.session_state.correct_synonyms = synonyms_list
    st.session_state.wrong_words = distractors
    

# Button to start new round
if st.button("Play"):
    load_new_round()

if st.session_state.choices:
    st.subheader(f"Find the synonyms for: {st.session_state.word}")
    user_guess = st.multiselect("Select the synonyms:", options=st.session_state.choices)

    if st.button("Check"):
        correct = [opt for opt in user_guess if opt in st.session_state.correct_synonyms]
        incorrect = [opt for opt in user_guess if opt in st.session_state.wrong_words]

        if len(incorrect) > 0:
            st.write(f"❌ Incorrect")
        elif len(correct) == len(st.session_state.correct_synonyms):
            st.write(f"✅ Correct")
            st.session_state.score = st.session_state.score +1
        elif len(correct) < len(st.session_state.correct_synonyms):
            st.write(f" Some correct words")
         
        st.write(f"The score is: {st.session_state.score}")
        st.info(f"The correct synonyms were: {st.session_state.correct_synonyms}")
        
        if st.button("Next word"):
            st.session_state.choices = []
            st.session_state.correct_synonyms = []
            st.session_state.wrong_words = []
            st.session_state.word = ""
            st.session_state.score = st.session_state.score
