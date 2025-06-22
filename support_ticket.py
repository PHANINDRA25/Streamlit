import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime 
from dateutil.relativedelta import relativedelta

'# Support Ticket Workflow'

# Set up input widgets
st.logo(image="streamlit-logo-primary-colormark-lighttext.png", 
        icon_image="streamlit-mark-color.png")

st.info('To write a ticket, fill out the form below. Check status or review ticketing analytics using the tabs below.')
tab1,tab2=st.tabs(['Write a ticket','Ticket Status and Analytics'])


def display_message():
    st.success('Ticket submitted successfully!')
    p=st.session_state.df['ID'].str[-4:].astype(int).max()+1
    a=pd.DataFrame([{'ID':f'TICKET-{p}','Issue':st.session_state.issue,'Status':'Open','Priority':st.session_state.Priority,'Date Submitted':datetime.now().date()}])
    st.dataframe(a,hide_index=True,use_container_width=True)
    st.session_state.df=pd.concat([st.session_state.df,a])
    st.session_state.df=st.session_state.df.sort_values('ID',ascending=False)
    #st.dataframe(st.session_state.df)



@st.cache_data
def load_data():
    df=pd.read_csv(r'support.csv')
    df['Date Submitted'] = pd.to_datetime(df['Date Submitted'])
    df['Date Submitted']=df['Date Submitted'].dt.date
    return df

if 'df' not in st.session_state:
    st.session_state.df=load_data()

with tab1:
    with st.form('my_form'):
        issue=st.text_area('Description of issue',key='issue')
        priority=st.selectbox('Priority',options=['High','Medium','Low'],key='Priority')
        submitted=st.form_submit_button('Submit')

        if submitted:
            display_message()



with tab2:
    '## Support Ticket Status'
    st.write('No. of tickets:',st.session_state.df.shape[0])
    '#### Things to try:'
    st.info('1️⃣ Update Ticket Status or Priority and see how plots are updated in real-time!')
    st.success('2️⃣ Change values in Status column from "Open" to either "In Progress" or "Closed", then click on the Sort DataFrame by the ' \
    'Status column button to see the refreshed DataFrame with the sorted Status column.')
    df1=st.session_state.df.sort_values(by='ID', ascending=False)
    st.dataframe(df1[['ID','Issue','Status','Priority','Date Submitted']].head(5),hide_index=True,use_container_width=True)

    '#### Support Ticket Analytics'
    col=st.columns(2)

    with col[0]:
        st.metric('First response time (hr)',value=5.2,delta=-0.5)
        st.metric('Open tickets',value=st.session_state.df[st.session_state.df['Status']=='Open'].shape[0])
        st.metric('Avg.resolution time (hr)', value=16, delta='')

    with col[1]:
        #st.subheader('')
        st.session_state.df['Date Submitted']= pd.to_datetime(st.session_state.df['Date Submitted'])
        st.session_state.df['month']=st.session_state.df['Date Submitted'].dt.month_name()
        df1=st.session_state.df[st.session_state.df['Date Submitted']>=datetime(2024,6,1)]
        df2=df1.groupby(['month','Status'])['Status'].count().rename('count').reset_index()
        st.bar_chart(data=df2,x='month',y='count',color='Status')

    




