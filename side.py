#module for the side bar content
import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
def sidebar():
    with st.sidebar:
        st.markdown("<h1 style='font-style: italic; color: #F55F0E;'>Hello Buddy !</h1>", unsafe_allow_html=True)
        st.write("")

        st.subheader("ABOUT:")
        st.markdown("ResearchBuddy empowers research scholars with AI technology, "
                    " allowing you to upload research papers and receive quick and "
                    "accurate answers to your questions, all powered by LangChain Model & OpenAI's advanced technology ")
        st.write("")
        st.write("")
        api_key_input = st.text_input(
            "Enter your OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )
        if api_key_input:
            set_openai_api_key(api_key_input)
        st.subheader("HOW TO USE: ")
        st.markdown("<p style = 'cursor: default;'>1.Enter your Open AI's API KEY."
                    "<br>2. Upload your research paper through the upload button."
                    "<br>3. Type your question in the text box."
                    "<br>4. Click 'Submit'."
                    "<br>5. Relax while we extract your answer."
                    "<br>6.  Hurray! your answer's here!!", unsafe_allow_html=True)

        lottie_animation_1 = "https://assets5.lottiefiles.com/packages/lf20_kv7kbdzp.json"
        lottie_anime_json = load_lottie_url(lottie_animation_1)
        st_lottie(lottie_anime_json, key="research")

