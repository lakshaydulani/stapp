from openai import OpenAI
import streamlit as st
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
from mdhandle import extract_section
from clipa import get_all_images_score

os.environ["LLAMA_CLOUD_API_KEY"] = st.secrets["LLAMA_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-3.5-turbo-0125")
Settings.llm = llm

st.title("Report Parser")

uploaded_file = st.file_uploader("Choose a file (PPTX only)")



if uploaded_file is not None:    
    bytes_data = uploaded_file.getvalue()
    filename = "./samplereport.pptx"
    
    
    with st.spinner('Working...'):
        with open(filename, 'wb') as f: 
            f.write(bytes_data)   
            
               
        documents_with_instruction = LlamaParse(
                                        result_type="markdown",
                                        ).load_data("./samplereport.pdf")
        
        
        if(len(documents_with_instruction) == 0):
            st.error("Some error in processing this report.")
        else:
            ref = documents_with_instruction[0].text
            st.title("Parsed Document - ")  
            
            st.markdown(ref)
        
