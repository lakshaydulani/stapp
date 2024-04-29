import requests
import base64
from glob import glob
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14"
headers = {"Authorization": "Bearer " + st.secrets["HF_KEY"]}

def query(data):
	with open(data["image_path"], "rb") as f:
		img = f.read()
	payload={
		"parameters": data["parameters"],
		"inputs": base64.b64encode(img).decode("utf-8")
	}
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


def get_all_images_score(topic, images):
	results = []
	for image in images:
		results.append((get_text_image_score(topic, image), image))

	for tuple in results:
		if(tuple[0] == topic):
			return tuple[1]	
 
	return None


def get_text_image_score(topic, image): 
    output = query({
        "image_path": image,
        "parameters": {"candidate_labels": [topic,"company logo", "person image"]},
    })
    return output[0]["label"]

if __name__ == "__main__":
	output = get_all_images_score("Stainless Steel Bottle Insulator", glob("imgs/*.*"))
	print(type(output[0]))