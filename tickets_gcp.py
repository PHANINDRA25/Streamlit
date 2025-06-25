from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
import pandas as pd

@st.cache_data
def authenticate_and_load_data():

    # === CONFIGURATION ===
    key_path = "symbolic-path-409308-9442c9b54782.json"  # Replace with your local path
    project_id = "symbolic-path-409308"
    dataset_id = "discovery"
    table_id = "tickets"

    # === AUTHENTICATE AND INIT CLIENT ===
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials, project=project_id)

    # === FULL TABLE ID ===
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # === LOAD TABLE INTO DATAFRAME ===
    df = client.list_rows(table_ref).to_dataframe()
    df=pd.DataFrame(df)

    return df

df= authenticate_and_load_data()

with st.expander('Data'):
    st.dataframe(df.head(5), use_container_width=True, hide_index=True)

with st.sidebar:
    st.subheader('Filter options')
    region=st.multiselect('Select Region', df['region'].unique().tolist(),default='East')
    channel=st.multiselect('Select Channel', df['channel'].unique().tolist(),default='Chat')
    ticket=st.multiselect('Select Ticket type', df['ticket_type'].unique().tolist(),default='Technical')

filter=df[df['region'].isin(region)&df['channel'].isin(channel)&df['ticket_type'].isin(ticket)]

# filter.groupby(['region','channel','ticket_type']).agg(
# Total_Tickets=('ticket_id','count'),
# Average_Resolution_Time_hr=('resolution_time_hours','mean'),
# Tickets_breached_SLA=('','')

# )

col=st.columns(3)
col[0].metric('# Tickets',value=filter.shape[0],border=True)
col[1].metric('Average resolution Time (hr)',value=filter['resolution_time_hours'].mean().round(),border=True)
col[2].metric('Escalated tickets (%)',value=(filter['escalated'].sum()/filter.shape[0]*100).round(),border=True)

with st.expander('Visuals'):
    st.subheader('Line chart: Avg Resolution Time over time')
    st.line_chart(data=filter,x='created_at',y='resolution_time_hours',use_container_width=True)
    st.subheader('Bar chart: Total Tickets by Ticket Type')
    st.bar_chart(data=filter.groupby('ticket_type').count().reset_index(),x='ticket_type',y='ticket_id',use_container_width=True)


