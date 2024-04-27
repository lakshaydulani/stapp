from openai import OpenAI
import streamlit as st
import pandas as pd
from io import StringIO
import os
from llama_parse import LlamaParse
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core.node_parser import MarkdownElementNodeParser
from getimgs import save_images 
from sentenceunderstanding import isSimilar
from glob import glob


os.environ["LLAMA_CLOUD_API_KEY"] = st.secrets["LLAMA_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-3.5-turbo-0125")
Settings.llm = llm

st.title("Inspection Report Analyzer")

uploaded_file = st.file_uploader("Choose a file (PDF only)")

if uploaded_file is not None:    
    bytes_data = uploaded_file.getvalue()
    cwd = os.getcwd()
    filename = os.path.join(cwd, "samplereport.pdf")
    
    with st.spinner('Working..'):
        with open(filename, 'wb') as f: 
            f.write(bytes_data)
        
        save_images()
            
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        if prompt := st.chat_input("Ask your questions about the document"):
            
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
         

            documents_with_instruction = LlamaParse(
                                            result_type="markdown",
                                                parsing_instruction="""
                                            This document is a report.
                                            Output all the tables as it is.""",
                                            ).load_data("samplereport.pdf")
            
            tab1, tab2 = st.tabs(["Chatbox", "Parsed Report"])
            tab2.markdown()
            tab2.download_button("Download",documents_with_instruction[0].text)

            with tab1:
                node_parser_instruction = MarkdownElementNodeParser(llm=OpenAI(model="gpt-3.5-turbo-0125"), num_workers=8)
                
                nodes_instruction = node_parser_instruction.get_nodes_from_documents(documents_with_instruction)
                (base_nodes_instruction,objects_instruction,) = node_parser_instruction.get_nodes_and_objects(nodes_instruction)

                recursive_index_instruction = VectorStoreIndex(nodes=base_nodes_instruction + objects_instruction)
                
                query_engine_instruction = recursive_index_instruction.as_query_engine(similarity_top_k=25)
            
            
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                    
                if(isSimilar(prompt, "show the image")):
                    with st.chat_message("assistant"):   
                        st.image("imgs/image1_1.png", caption="image1_1.png")
                else:
                    response_1_i = query_engine_instruction.query(prompt)
                    with st.chat_message("assistant"):                    
                        st.markdown(response_1_i)
                    st.session_state.messages.append({"role": "assistant", "content": response_1_i})
                    