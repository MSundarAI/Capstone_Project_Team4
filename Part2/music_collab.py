__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

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

st.set_page_config(page_title="CA Collab", page_icon="🎹", layout="wide")
# Set title
st.image('./Part2/images/logo.png', width=100,caption = None)
st.title("CA Collaboration Tool", anchor=False)
st.header("Find out who you should collalborate with to reach the next step in your musical journey", anchor=False)

# Select variables
st.divider()
loudness = st.slider('Select a loudness value', min_value=1, max_value=10)
danceability = st.slider('Select a danceability value', min_value=1, max_value=10)

# Submit button
st.divider()
submit_button = st.button('Find Best Match')

# display openai key message
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
st.write(openai_api_key)
st.write("Current working directory:", os.getcwd())


def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))


def collab(danceability,openai_api_key):
  
    file_path = './Part2/data/training.csv'
    os.environ["OPENAI_API_KEY"] = openai_api_key
    # Load the dataset
    loader = CSVLoader(file_path=file_path,encoding="utf-8")
    
    # Create an index using the loaded documents
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])
   
    chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")
   
    # Run the chain
    query = "if my danceability is" + str(danceability) + ", what artist should I collaborate with"
    response = chain({"question": query})
    return response['result']

# checking if variables have value
if submit_button and danceability:
    with st.spinner("Processing..."):
        summary = collab(danceability,openai_api_key)
        
        # Show Summary
        st.subheader("Summary:", anchor=False)
        st.write(summary)