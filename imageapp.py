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

def get_images_with_text_pagewise(filename = "./imagespdf.pdf"):
    output = []
    pdf_file = fitz.open(filename)
    foldername = "images"
    
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    else:
        for f in os.listdir(foldername):
            os.remove(os.path.join(foldername, f))            
    
    for page_index in range(len(pdf_file)):
        pageoutput = []
        page = pdf_file[page_index]
        image_list = page.get_images()
        txt = page.get_text()
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
            
        for image_index, img in enumerate(page.get_images(), start=1):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            name = f"image{page_index+1}_{image_index}.{image_ext}"
            output.append(name)
            image.save(open(f"{foldername}/{name}", "wb"))    
        output.append({"page": page_index, "text": txt, "images": output})
    
    #save output as json
    with open("output.json", "w") as f:
        json.dump(output, f)
        

os.environ["LLAMA_CLOUD_API_KEY"] = st.secrets["LLAMA_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.title("PDF Images Analyzer")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:    
    bytes_data = uploaded_file.getvalue()
    filename = "./imagespdf.pdf"
    
    with st.spinner('Working...'):
        with open(filename, 'wb') as f: 
            f.write(bytes_data)
            prcs(filename, st)
            st.json("./output.json")
