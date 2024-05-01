import requests
import streamlit as st

api_token = st.secrets["HF_KEY"]
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()



def isSimilar(sentence, ref):
    return sentence in ["show me the image", "show me the image of the product in the report", "show the image", "what is the image", "whats the image", "show me the product", "show me the product photo"]
    data = query(
    {
        "inputs": {
            "source_sentence": ref,
            "sentences":[sentence]
        }
    })
    return (data[0] >= 0.65)    