import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from sklearn.ensemble import RandomForestClassifier

'# Penguin Species Prediction App'
st.write(' ')
st.write(' ')
with st.expander('Data'):
    st.write('**Raw data**')
    df=pd.read_csv(r'https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
    st.dataframe(df, use_container_width=True)

    st.write('**X**')
    X_raw=df.drop('species',axis=1)
    st.dataframe(X_raw, use_container_width=True)

    st.write('**y**')
    y_raw=df['species']
    st.dataframe(y_raw, use_container_width=True)


with st.expander('Data Visualization'):
    st.scatter_chart(data=df,x='bill_length_mm',y='body_mass_g',color='species')

with st.sidebar:
    st.subheader('Input features')
    island=st.selectbox('Island',['Biscoe','Dream','Torgersen'])
    bill_length=st.slider('Bill length (mm)',32.1,59.6,43.9)
    bill_depth=st.slider('Bill depth (mm)',13.1,21.5,17.2)
    flipper_length=st.slider('Flipper length (mm)',172,231,201)
    body_mass=st.slider('Body mass (g)',2700,6300,4207)
    gender=st.selectbox('Gender',['male','female'])



with st.expander('Input features'):
    st.write('**Input penguin**')
    input_df=pd.DataFrame({'island':island,
                           'bill_length_mm':bill_length,'bill_depth_mm':bill_depth,
                           'flipper_length_mm':flipper_length,'body_mass_g':body_mass,'sex':gender},index=[0])
    st.dataframe(input_df, use_container_width=True)
    st.write('**Combined penguins data**')
    df1=pd.concat([X_raw,input_df],axis=0)
    st.dataframe(df1, use_container_width=True)

with st.expander('Data Preparation'):
    st.write('**Encoded X (input penguin)**')
    encode=['island','sex']
    df_penguins=pd.get_dummies(df1,prefix=encode)
    l={'Adelie': 0, 'Chinstrap': 1,'Gentoo': 2}
    y=y_raw.map(l)
    input_df1=df_penguins.iloc[-1]
    X=df_penguins[:-1]
    input_df2 = pd.DataFrame([input_df1])
    #input_df2=pd.DataFrame(input_df1, index=[0]).T

    st.dataframe(input_df2)
    st.write('**Encoded y**')
    st.dataframe(pd.DataFrame(y,columns=['species']), use_container_width=True)


clf = RandomForestClassifier()
clf.fit(X, y)
prediction=clf.predict(input_df2)
prediction_proba =clf.predict_proba(input_df2)
df_prediction_proba =pd.DataFrame(prediction_proba)
df_prediction_proba.columns = ['Adelie', 'Chinstrap', 'Gentoo']
df_prediction_proba.rename(columns={0: 'Adelie',
                                 1: 'Chinstrap',
                                 2: 'Gentoo'})
st.dataframe(df_prediction_proba,column_config={'Adelie':st.column_config.ProgressColumn('Adelie',format='%f',min_value=0,max_value=1),
                                                'Chinstrap':st.column_config.ProgressColumn('Chinstrap',format='%f',min_value=0,max_value=1),
                                                'Gentoo':st.column_config.ProgressColumn('Gentoo',format='%f',min_value=0,max_value=1)})
df_prediction_proba
temp=0
name=''
for i in df_prediction_proba.columns:
    
    if temp<=df_prediction_proba[i].iloc[0]:
        temp=df_prediction_proba[i].iloc[0]
        name=i

st.success(name)


