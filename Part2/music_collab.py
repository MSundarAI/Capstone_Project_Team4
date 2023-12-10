import streamlit as st
import pandas as pd
import openai
from langchain.llms import OpenAI
from langchain.chains import  LLMChain
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
import os


openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))


def collab(danceability):
  
    file_path = '/data/training.csv'
  
    # Load the dataset
    loader = CSVLoader(file_path=file_path)
    
    # Create an index using the loaded documents
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])
   
    chain = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0.7, openai_api_key=openai_api_key), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")
   
    # Run the chain
    query = "if my danceability is" + str(danceability) + ", what artist should I collaborate with"
    response = chain({"question": query})
    return response['result']

# Set page title
st.set_page_config(page_title="Team CA", page_icon="🎹", layout="wide")


# Set title
st.title("Team CA Collaboration Tool", anchor=False)
st.header("Find out who you should collalborate with to reach the next step in your musical journey", anchor=False)

# Select variables
st.divider()
loudness = st.slider('Select a loudness value', min_value=1, max_value=10)
danceability = st.slider('Select a danceability value', min_value=1, max_value=10)

# Submit button
st.divider()
submit_button = st.button('Find Best Match')

# checking if variables have value
if submit_button and danceability:
    with st.spinner("Processing..."):
        summary = collab(danceability)
        
        # Show Summary
        st.subheader("Summary:", anchor=False)
        st.write(summary)