from openai import OpenAI
import streamlit as st
import pandas as pd
from io import StringIO
import os

os.environ["LLAMA_CLOUD_API_KEY"] = st.secrets["LLAMA_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-3.5-turbo-0125")
Settings.llm = llm

from llama_parse import LlamaParse

st.title("MSIL Inspection Report Analyzer")
st.subheader("Upload the file: (PDF only)")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # get current cwd python
    cwd = os.getcwd()
    filename = os.path.join(cwd, "samplereport.pdf")

    with open(filename, 'wb') as f: 
        f.write(bytes_data)

    documents_with_instruction = LlamaParse(
    result_type="markdown",
    parsing_instruction="""
This document is an inspection report.
Output all the tables as it is.
Output the Product photo. """,
).load_data("samplereport.pdf")
    
    print(documents_with_instruction)

    st.markdown(documents_with_instruction[0].text)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your questions about the document"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(prompt)

    # with st.chat_message("assistant"):
    #     stream = client.chat.completions.create(
    #         model=st.session_state["openai_model"],
    #         messages=[
    #             {"role": m["role"], "content": m["content"]}
    #             for m in st.session_state.messages
    #         ],
    #         stream=True,
    #     )
    #     response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": prompt})
