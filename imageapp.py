from openai import OpenAI
import streamlit as st
import os
from glob import glob
import fitz
from PIL import Image
import io
import os
import json
from imageanalysis import prcs

st.title("PDF Images Analyzer")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:    
    bytes_data = uploaded_file.getvalue()
    filename = "./imagespdf.pdf"
    
    with st.spinner('Working...'):
        with open(filename, 'wb') as f: 
            f.write(bytes_data)
            prcs(filename, st)
            # st.json("./output.json")
