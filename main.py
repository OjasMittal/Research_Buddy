import streamlit as st
import base64
from openai.error import OpenAIError
from tools import (
    embed_docs,
    get_answer,
    get_sources,
    parse_docx,
    parse_pdf,
    parse_txt,
    search_docs,
    text_to_docs,
)
from side import sidebar

def clear_submit():
    st.session_state["submit"] = False
st.session_state["OPENAI_API_KEY"] = st.secrets["pass"]
st.set_page_config(page_title="Research Buddy", page_icon="📖")
sidebar()
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

# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
#         background-size: 100%;
#         background-repeat: no-repeat;
#         background-position: bottom;
#         background-color: rgba(255,255,255,0.5);
#     }}
#     [data-testid="stHeader"]{{
# background-color: rgba(0,0,0,0);
# }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )
# add_bg_from_local('background.avif')

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
            sources = get_sources(answer, sources)
            st.markdown("#### Answer")
            st.markdown(answer["output_text"].split("SOURCES: ")[0])
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.markdown("#### Sources")
            for source in sources:
                st.markdown(source.page_content)
                st.markdown(source.metadata["source"])
                st.markdown("---")
        except OpenAIError as e:
            st.error(e._message)