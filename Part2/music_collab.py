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
tempo = st.slider('Select a tempo value', 1, 250,step=1)
loudness = st.slider('Select a loudness value', -60, 0,step=1)
danceability = st.slider('Select a danceability value', 0.0, 1.0,step=0.1)
liveness = st.slider('Select a liveness value', 0.0, 1.0,step=0.1)
energy = st.slider('Select a energy value', 0.0, 1.0,step=0.1)
duration = st.slider('Select a duration_ms value', 100000, 400000,step=50000)
acousticness = st.slider('Select a acousticness value',0.0, 1.0,step=0.1)
instrumentalness = st.slider('Select a instrumentalness value',0.0, 1.0,step=0.1)

# Submit button
st.divider()
submit_button = st.button('Find Best Match')

# display openai key message
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
st.write("API key entered:",openai_api_key)



def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))


def collab(danceability,tempo,energy,loudness,liveness,duration,acousticness,instrumentalness,openai_api_key):
  
    file_path = './Part2/data/demo.csv'
    os.environ["OPENAI_API_KEY"] = openai_api_key
    # Load the dataset
    loader = CSVLoader(file_path=file_path,encoding="utf-8")
    
    # Create an index using the loaded documents
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])
   
    chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")
   
    # Run the chain
    query = "if my danceability is" + str(danceability)  + ", if my tempo is " + str(tempo) + ", if my energy is " + str(energy) + ", if my loudness is " + str(loudness) + ", if my liveness is " + str(liveness) + ", if my duration is " + str(duration) + ", if my acousticness is " + str(acousticness) + ", if my instrumentalness is " + str(instrumentalness)  + ", what artist should I collaborate with, give me the best 1 recommendation that you can"
    response = chain({"question": query})
    return response['result']

# checking if variables have value
if submit_button:
    with st.spinner("Processing..."):
        artist_to_collab = collab(danceability,tempo,energy,loudness,liveness,duration,acousticness,instrumentalness,openai_api_key)
        # Recommendations
        st.subheader("Artist Recommendation:", anchor=False)
        st.write(artist_to_collab)
