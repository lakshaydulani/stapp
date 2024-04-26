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
    bytes_data = uploaded_file.getvalue()
    cwd = os.getcwd()
    filename = os.path.join(cwd, "samplereport.pdf")

    with open(filename, 'wb') as f: 
        f.write(bytes_data)

    with st.spinner('Working on the document..'):
        documents_with_instruction = LlamaParse(
                                        result_type="markdown",
                                            parsing_instruction="""
                                        This document is an inspection report.
                                        Output all the tables as it is.
                                        Output the Product photo. """,
                                        ).load_data("samplereport.pdf")
    
    st.markdown(documents_with_instruction[0].text)
    
    from llama_index.core.node_parser import MarkdownElementNodeParser

    node_parser_instruction = MarkdownElementNodeParser(
    llm=OpenAI(model="gpt-3.5-turbo-0125"), num_workers=8
)
    
    nodes_instruction = node_parser_instruction.get_nodes_from_documents(documents_with_instruction)
    (
    base_nodes_instruction,
    objects_instruction,
    ) = node_parser_instruction.get_nodes_and_objects(nodes_instruction)

    recursive_index_instruction = VectorStoreIndex(
        nodes=base_nodes_instruction + objects_instruction
    )
    
    query_engine_instruction = recursive_index_instruction.as_query_engine(
        similarity_top_k=25
    )
    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if prompt := st.chat_input("Ask your questions about the document"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response_1_i = query_engine_instruction.query(prompt)
            st.markdown(response_1_i)
            st.session_state.messages.append({"role": "assistant", "content": response_1_i})
    
    
