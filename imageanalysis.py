import streamlit as st
import os
from glob import glob
import fitz
from PIL import Image
import io
import os
import json
from textblob import TextBlob
from clipa import get_text_image_score

def images_with_text_pagewise(filename = "reffiles/pdf.pdf"):
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
        txt = page.get_text("blocks")

        txts = [block_text[4] for block_text in txt if block_text[4] != " \n"]
        # print(txts)
        
        # blob = TextBlob(txts) 
        # print(blob.noun_phrases)
        
                    
        for image_index, img in enumerate(page.get_images(), start=1):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            name = f"image{page_index+1}_{image_index}.{image_ext}"
            pageoutput.append(name)
            image.save(open(f"{foldername}/{name}", "wb"))    
        # output.append({"page": page_index, "text": blob.noun_phrases, "images": pageoutput})
        output.append({"page": page_index, "text": txts, "images": pageoutput})
    
    #save output as json
    with open("output.json", "w") as f:
        json.dump(output, f)
        
def filter_topics(topics):
    # remove duplicates from topics
    topics = list(set(topics))
    #sort the list 'topics' in decreasing order of word count
    topics.sort(key=lambda x: len(x.split()), reverse=True)
    #take first 10
    return topics[:10]
    
def prcs(filename, st):
    images_with_text_pagewise(filename)
    match_images_with_text_using_clip("output.json",st)
    
        
def match_images_with_text_using_clip(filename,st):
    
    output = []
    with open(filename) as f:
        data = json.load(f)
        for page in data:
            imgs = page["images"]
            topics = page["text"]
            
            filteredtopics = filter_topics(topics)
            
            
            if(len(imgs) > 0):
                #loop over page["images"]
                for img in imgs:
                    try:
                        clip_topic = get_text_image_score(filteredtopics, f"images/{img}")
                        if(st is not None):
                            st.image(f"images/{img}", caption=clip_topic)
                        output.append({"image": img, "clip_topic": clip_topic})
                    except:
                        output.append({"image": img, "clip_topic": "error in clip endpoint"})
                    #save output as json
    
    with open("images_topics.json", "w") as f:
        json.dump(output, f)
                    
         
if __name__ == "__main__":
    images_with_text_pagewise()
    # match_images_with_text_using_clip()
 