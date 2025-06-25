import streamlit as st
import pandas as pd
import numpy as np
import datetime  as dt
from statsmodels.tsa.arima.model import ARIMA
import altair as alt

'# Sales Forecasting App'
def load_data():
    file=st.file_uploader('Upload the file',type=['csv','xlsx'])
    return file
file=load_data()

''
''

tab1,tab2=st.tabs(['Data Exploration Tab','Forecasting Tab'])

with st.sidebar:
    store=st.multiselect('Select Store',['Store A', 'Store B', 'Store C'])
    product=st.multiselect('Select Product',['Product X', 'Product Y', 'Product Z'])
    forecast=st.selectbox('Forecast_horizon',['30 days','60 days','90 days'])


with tab1:
    if file is not None and store and product:

        st.markdown('')
        '### Summary Statistics'
        df=pd.read_csv(file)
        filter=df[df['Store'].isin(store) & df['Product'].isin(product)]
        result = filter.groupby(['Store', 'Product']).agg(
        Total_revenue=('Revenue', 'sum'),
        Avg_units_sold=('Units Sold', 'mean')
        ).reset_index()

        result['Avg_units_sold'] = result['Avg_units_sold'].round()
        st.dataframe(result,hide_index=True)

        # with st.sidebar:
        #     st.subheader('Date Options')
        #     start_date=st.date_input('Start Date',min=datetime.date(2021,1,1),max=datetime.date(2023,12,31),
        ''
        '### Line chart of Revenue'
        st.line_chart(data=filter,x='Date',y='Revenue',use_container_width=True)
        ''
        '### Bar chart of Total Revenue by Product'
        st.bar_chart(data=result,x='Product',y='Total_revenue',use_container_width=True)

with tab2:
    if file is not None and store and product and forecast:
        def forecast1(forecast):
            df1=df.groupby('Date')['Revenue'].sum()
            df1=pd.DataFrame(df1)

            #daily_revenue = df1['Revenue'].resample('D').mean().interpolate()
            # Step 3: Fit ARIMA model
            model = ARIMA(df1, order=(1, 1, 1))
            model_fit = model.fit()

            # Step 4: Forecast next 30 days
            forecasted_value = model_fit.forecast(steps=int(forecast.split(' ')[0]))
            forecasted_value_df=pd.DataFrame(forecasted_value).reset_index().rename(columns={'predicted_mean':'Revenue','index':'Date'})
            forecasted_value_df.Date=forecasted_value_df.Date.dt.date
            #forecasted_value_df.index=forecasted_value_df.index.dt.date
            #date_df=df.set_index('Date')
            tail=df1.tail(90).reset_index().rename(columns={'index':'Date'})
            
            combined_data=pd.concat([tail,forecasted_value_df]).reset_index()
            st.subheader('Forecasting Results')
            ''
            
            st.line_chart(data=combined_data,x='Date',y='Revenue',use_container_width=True)

        

        forecast1(forecast)









    





        


