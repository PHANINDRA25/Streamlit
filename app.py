import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title='YouTube Channel Dashboard',layout='wide')


@st.cache_data
def load_data():
    data=pd.read_csv(r'youtube_channel_data.csv')
    data['DATE'] = pd.to_datetime(data['DATE'])
    data['NET_SUBSCRIBERS']=data['SUBSCRIBERS_GAINED']-data['SUBSCRIBERS_LOST']
    return data

def aggregate_data(df, time_frame,y,color):
    freq_map={"Daily": "D", "Weekly": "W", "Monthly": "M"}
    selected_freq =freq_map[time_frame]

    df=df.set_index("DATE")
    agg_df=df.resample(selected_freq).sum()
    agg_df=agg_df.reset_index()
    st.bar_chart(data=agg_df,x='DATE',y=y,y_label=y,color=color,use_container_width=True)

def duration_data(df, start_date, end_date, time_frame, y, color,chart_selection):
        freq_map={"Daily": "D", "Weekly": "W", "Monthly": "M"}
        selected_freq =freq_map[time_frame]
        filtered_df=df[(df['DATE']>=pd.to_datetime(start_date)) & (df['DATE']<=pd.to_datetime(end_date))]
        filtered_df=filtered_df.set_index("DATE")
        agg_df=filtered_df.resample(selected_freq).sum()
        agg_df=agg_df.reset_index()

        current_value = df[value[i]].iloc[-1]
        previous_value = df[value[i]].iloc[-2]
        delta = current_value - previous_value
        delta_percent = (delta / previous_value) * 100 if previous_value != 0 else 0
        delta_str = f"{delta:+,.0f} ({delta_percent:+.2f}%)"
        value1=df[(df['DATE']>=pd.to_datetime(start_date)) & (df['DATE']<=pd.to_datetime(end_date))][value[i]].sum()
        value1=f"{value1:,.0f}"
        st.metric(heading[i],value=value1,delta=delta_str,delta_color="normal")

        chart_selection=chart_selection.lower()
        if chart_selection == 'area':
            st.area_chart(data=agg_df,x='DATE',y=y,color=color,y_label=y,use_container_width=True)
        else:
            st.bar_chart(data=agg_df,x='DATE',y=y,color=color,y_label=y,use_container_width=True)



           
                   

df=load_data()

# Set up input widgets
st.logo(image="streamlit-logo-primary-colormark-lighttext.png", 
        icon_image="streamlit-mark-color.png")

with st.sidebar:

    st.header('YouTube Channel Dashboard')
    st.subheader('⚙️ Settings')
    max_date=df['DATE'].max().date()
    default_start_date=max_date-timedelta(days=365)
    default_end_date=max_date

    start_date=st.date_input('Start date',value=default_start_date,max_value=max_date,min_value=df['DATE'].min().date())
    end_date=st.date_input('End date',value=default_end_date,max_value=max_date,min_value=df['DATE'].min().date())
    time_frame=st.selectbox('Select time frame',["Daily", "Weekly", "Monthly"])
    chart_selection = st.selectbox("Select a chart type", ("Bar", "Area"))

st.subheader('All-Time Statistics')
cols=st.columns(4,border=True)


heading=['Total Subscribers','Total Views','Total Watch Hours','Total Likes']
value=['NET_SUBSCRIBERS','VIEWS','WATCH_HOURS','LIKES']
color=['#00BFFF', '#FFA500', '#EE609C', '#9B59B6']
for i in range(4):
    with cols[i]:
        current_value = df[value[i]].iloc[-1]
        previous_value = df[value[i]].iloc[-2]
        delta = current_value - previous_value
        delta_percent = (delta / previous_value) * 100 if previous_value != 0 else 0
        delta_str = f"{delta:+,.0f} ({delta_percent:+.2f}%)"
        a=df[value[i]].sum()
        value1=f"{a:,.0f}"
        st.metric(heading[i],value=value1,delta=delta_str,delta_color="normal")
        aggregate_data(df, time_frame,value[i],color[i])


st.subheader('Selected Duration')
cols=st.columns(4,border=True)

heading1=['Subscribers','Views','Watch Hours','Likes']
value=['NET_SUBSCRIBERS','VIEWS','WATCH_HOURS','LIKES']
color=['#00BFFF', '#FFA500', '#EE609C', '#9B59B6']


for i in range(4):
    with cols[i]:
        duration_data(df, start_date, end_date, time_frame, value[i], color[i],chart_selection)


def drop_down(df, start_date, end_date, time_frame):
        freq_map={"Daily": "D", "Weekly": "W", "Monthly": "M"}
        selected_freq =freq_map[time_frame]
        filtered_df=df[(df['DATE']>=pd.to_datetime(start_date)) & (df['DATE']<=pd.to_datetime(end_date))]
        filtered_df=filtered_df.set_index("DATE")
        agg_df=filtered_df.resample(selected_freq).sum()
        agg_df=agg_df.reset_index()
        st.dataframe(agg_df[['DATE','VIEWS', 'WATCH_HOURS','NET_SUBSCRIBERS', 'LIKES','COMMENTS','SHARES']], use_container_width=True, hide_index=True)

     


with st.expander("See DataFrame (Selected time frame)"):
    drop_down(df,start_date, end_date, time_frame)








