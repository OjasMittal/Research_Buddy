import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def sidebar():
    with st.sidebar:
        st.markdown("<h1 style='font-style: italic; color: #F55F0E;'>Hello Buddy !</h1>", unsafe_allow_html=True)
        st.write("")

        st.subheader("ABOUT:")
        st.markdown("Empowering research scholars with AI technology, "
                    "Research Buddy  allows you to upload research papers and receive quick and "
                    "accurate answers to your questions, all powered by OpenAI's advanced technology ")
        st.write("")
        st.write("")

        st.subheader("HOW TO USE: ")
        st.markdown("<p style = 'cursor: default;'>1. Upload your research paper through the upload button."
                    "<br>2. Type your question on the text box."
                    "<br>3. Click 'Submit'."
                    "<br>4. Relax while we extract your answer."
                    "<br>5.  Hurray! your answer's here!!", unsafe_allow_html=True)

        lottie_animation_1 = "https://assets5.lottiefiles.com/packages/lf20_kv7kbdzp.json"
        lottie_anime_json = load_lottie_url(lottie_animation_1)
        st_lottie(lottie_anime_json, key="news")
