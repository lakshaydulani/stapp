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

#write a function in python that checks if a string is a substring of another paramter, and make it case insensitive
def is_substring(sub, main):
    # Convert both strings to lower case to make the search case-insensitive
    sub_lower = sub.lower()
    main_lower = main.lower()

    # Check if the lowercased substring exists within the lowercased main string
    return sub_lower in main_lower

os.environ["LLAMA_CLOUD_API_KEY"] = st.secrets["LLAMA_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-3.5-turbo-0125")
Settings.llm = llm

st.title("Report Analyzer")

option = st.selectbox(
    "What kind of document do you want to analyze?",
    ("Inspection Report", "Medical Report","General PDF"))

inspection_instruction_with_options = """This document is an inspection report.Preserve all the tables. Only if defects are mentioned in the document, create a separate section named 'Defects' and save information for columns {Critical, Major, Minor} and rows {AQL, Defects found, Max. allowed} in a separate table. Give each section their own heading"""

medical_instruction_with_options = """This document is a Medical blood report of a patient. Ignore Comments given in the document. 
Whenever there is a table with test result in the document, append it to a table with the following column values {TestName} and their {Result}.
The output should only have markdown tables prefixed with their heading. The markdown output should be sanitized"""

general_instruction_with_options = """Keep the tables in the document as it is."""

uploaded_file = st.file_uploader("Choose a file (PDF only)")



if uploaded_file is not None:    
    bytes_data = uploaded_file.getvalue()
    filename = "./samplereport.pdf"
    
    
    with st.spinner('Working...'):
        with open(filename, 'wb') as f: 
            f.write(bytes_data)
       
       
        instruction_with_options = general_instruction_with_options
        
        if(option == "Inspection Report"):
            save_images()
            instruction_with_options = inspection_instruction_with_options
        elif(option == "Medical Report"):
            instruction_with_options = medical_instruction_with_options
            
               
        documents_with_instruction = LlamaParse(
                                        result_type="markdown",
                                            parsing_instruction=instruction_with_options,
                                        ).load_data("./samplereport.pdf")
        
        
        if(len(documents_with_instruction) == 0):
            st.error("Some error in processing this report.")
        else:
            ref = documents_with_instruction[0].text
            st.title("Parsed Document")
            st.markdown(ref)
        
            # node_parser_instruction = MarkdownElementNodeParser(llm=OpenAI(model="gpt-3.5-turbo-0125"), num_workers=8)
            
            # nodes_instruction = node_parser_instruction.get_nodes_from_documents(documents_with_instruction)
            # (base_nodes_instruction,objects_instruction,) = node_parser_instruction.get_nodes_and_objects(nodes_instruction)

            # recursive_index_instruction = VectorStoreIndex(nodes=base_nodes_instruction + objects_instruction)
            
            # query_engine_instruction = recursive_index_instruction.as_query_engine(similarity_top_k=25)            
            
            # image = None     
            
            # if(is_substring("Stainless Steel Bottle Insulator", ref)):
            #     image = "imgs/image1_3.jpeg"
            
            # if "messages" not in st.session_state:
            #     st.session_state.messages = []
                
            # prompt = st.chat_input("Ask your questions about the document")        
            # if prompt:
            #     with st.chat_message("user"):   
            #         st.markdown(prompt)
            #     section_found = extract_section(prompt, ref)
            #     if(prompt == "show complete document"):
            #         st.markdown(ref)
            #     elif(isSimilar(prompt, "show the product image")):
            #         with st.chat_message("assistant"):   
            #             if(image is not None):
            #                 st.image(image)
            #             else:
            #                 if(image is None):
            #                     imgs = glob("imgs/*.*")
            #                     if(len(imgs) > 0):
            #                         st.write("Here are all the images in the document:")
            #                         for image in imgs:
            #                             st.image(image)
            #                     else:
            #                         st.write("No images found in the document")                               
            #     elif(section_found != "Section not found" and section_found != "Valid prefix not found"):
            #         out = extract_section(prompt, ref)
            #         st.markdown(out)
            #         st.session_state.messages.append({"role": "assistant", "content": out})
            #     else:
            #         response_1_i = query_engine_instruction.query(prompt)
            #         with st.chat_message("assistant"):                    
            #             st.markdown(response_1_i)
            #         st.session_state.messages.append({"role": "assistant", "content": response_1_i})
                    