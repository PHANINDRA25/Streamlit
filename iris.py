import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import requests
from io import BytesIO
import pickle



def load_model():
    
    url = 'https://storage.googleapis.com/model_iris34/iris_model1.pkl'
    response = requests.get(url)
    loaded_model = pickle.load(BytesIO(response.content))
    return loaded_model

model = load_model()
st.title('Iris Species Prediction App')

file=st.file_uploader("Upload a CSV file with iris data", type=["csv"])

# Convert to DataFrame
if file is not None:
    try:
        df = pd.read_csv(file)
        st.write('### Raw Data')
        st.dataframe(df, use_container_width=True)
        predictions = model.predict(df)

        df['target']=predictions
        '### Predictions'
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
else:
    st.info('Please upload a CSV file.')



