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

st.title("Inspection Report Analyzer")

uploaded_file = st.file_uploader("Choose a file (PDF only)")

if uploaded_file is not None:    
    bytes_data = uploaded_file.getvalue()
    filename = "./samplereport.pdf"
    
    with st.spinner('Working...'):
        with open(filename, 'wb') as f: 
            f.write(bytes_data)
        
        st.toast("Document has been uploaded..")
        
        save_images()       
               
        documents_with_instruction = LlamaParse(
                                        result_type="markdown",
                                            parsing_instruction="""
                                        This document is a report.
                                        Output all the tables as it is.""",
                                        ).load_data("samplereport.pdf")
        
        st.toast("Document has been processed..")
        
        ref = documents_with_instruction[0].text
    
        node_parser_instruction = MarkdownElementNodeParser(llm=OpenAI(model="gpt-3.5-turbo-0125"), num_workers=8)
        
        nodes_instruction = node_parser_instruction.get_nodes_from_documents(documents_with_instruction)
        (base_nodes_instruction,objects_instruction,) = node_parser_instruction.get_nodes_and_objects(nodes_instruction)

        recursive_index_instruction = VectorStoreIndex(nodes=base_nodes_instruction + objects_instruction)
        
        query_engine_instruction = recursive_index_instruction.as_query_engine(similarity_top_k=25)
        
        doc_summary = query_engine_instruction.query("what is the summary of the document")        
        st.markdown(doc_summary)
        
        product_name = query_engine_instruction.query("just tell the product name")     
        
        image = None
        
        try:
            if(product_name is not None):   
                st.markdown("The Product is : ")
                st.markdown(product_name)        
                image = get_all_images_score(product_name, glob("imgs/*.*"))
            else:
                get_all_images_score(product_name, glob("imgs/*.*"))
        except:
            st.error("Error in analyzing the images!")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        if prompt := st.chat_input("Ask your questions about the document"):
            with st.chat_message("user"):   
                st.markdown(prompt)
                
            section_found = extract_section(prompt, ref)
            if(isSimilar(prompt, "show the image")):
                with st.chat_message("assistant"):   
                    if(image is not None):
                        st.image(image)
                    else:
                        if(image is None):
                            imgs = glob("imgs/*.*")
                            if(len(imgs) > 0):
                                st.write("Here are all the images in the document:")
                                for image in imgs:
                                    st.image(image)
                            else:
                                st.write("No images found in the document")                               
                                
                        
            elif(section_found != "Section not found" and section_found != "Valid prefix not found"):
                out = extract_section(prompt, ref)
                st.markdown(out)
                st.session_state.messages.append({"role": "assistant", "content": out})
            else:
                response_1_i = query_engine_instruction.query(prompt)
                with st.chat_message("assistant"):                    
                    st.markdown(response_1_i)
                st.session_state.messages.append({"role": "assistant", "content": response_1_i})
                