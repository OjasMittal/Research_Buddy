#main module integrating the sub-modules
import requests
import streamlit as st
import emaill
from openai.error import OpenAIError
from side import sidebar
from tools import (
    embed_docs,
    get_answer,
    parse_docx,
    parse_pdf,
    parse_txt,
    search_docs,
    text_to_docs,
)

def clear_submit():
    st.session_state["submit"] = False
st.set_page_config(page_title="Research Buddy", page_icon="📖")
sidebar()
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
col1,col2=st.columns([1,6])
with col1:
    st.image("iconn.png")
with col2:
    st.markdown("<h1 style = 'margin-bottom:-5%;'>Research<span style= 'color: #F55F0E;'> Buddy</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style = 'padding-bottom: 10%'>~Effortless Happpy Research</p>",unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
    on_change=clear_submit,
)
inx = None
data = None
if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
        data = parse_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        data = parse_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        data = parse_txt(uploaded_file)
    else:
        raise ValueError("File type not supported!")
    text = text_to_docs(data)
    try:
        spinner_running = True
        with st.spinner("Indexing document... This may take a while⏳"):
            inx = embed_docs(text)
        st.session_state["api_key_configured"] = True
    except OpenAIError as e:
        st.error(e._message)
ques = st.text_area("Ask your question about the document", on_change=clear_submit)
button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("OpenAI API key is invalid !")
    elif not inx:
        st.error("Please upload a document!")
    elif not ques:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        sources = search_docs(inx, ques)
        try:
            answer = get_answer(sources, ques)
            st.markdown("#### Answer")
            if(len(sources)!=None):
                ans=answer["output_text"].split("SOURCES:")[0]
                st.markdown(ans)
            else:
                ans="Sorry no relevant answer could be found."
                st.markdown(ans)
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.markdown("#### Sources")
            if "I do not know" in answer["output_text"].split("SOURCES:")[0]:
                st.write("No relevant sources found!")
            else:
                for source in sources:
                    st.markdown(source.page_content)
                    st.markdown(source.metadata["source"])
                    st.markdown("---")
        except OpenAIError as e:
            st.error(e._message)
    st.info("To email the Answer, enter your email id and click on Send button.")
    email = st.text_input("Enter your email id")
    if st.button("Send"):
        auth=st.secrets["AUTH_TOKEN"]
        success = emaill.send_email(email,ans,auth)
        if success:
            st.success("Mail Sent Successfully!")
