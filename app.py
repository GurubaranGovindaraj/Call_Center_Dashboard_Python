import streamlit as st
import pandas as pd
import altair as alt
import datetime 
import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(
    page_title="📞Gurubaran_Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#st.markdown("# <h1 style='text-align: center; color: #87CEEB; margin-top:-100px; font-size: 35px'>CALL CENTER DASHBOARD</h1>", unsafe_allow_html=True)

df = pd.read_excel(r"./Call-Center-Dataset.xlsx")

#st.header('Data')
#st.write(df.head(5))

df['Date'] = pd.to_datetime(df['Date'])

with st.sidebar:
    st.title('📞Call Center Dashboard')
    select_agent = st.selectbox('Agent',['Select a Agent'] + list(df['Agent'].unique()))
    select_topic = st.selectbox('Topic',['Select a Topic'] + list(df['Topic'].unique()))
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date1 = st.date_input('Start Date',min_date)
    date2 = st.date_input('End Date',max_date)
    
if date1 < date2:
    if date1 and date2:
        start_date,end_date = date1,date2
        df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
else:
    st.error("Check Your Date")


if select_agent == 'Select a Agent':
    df = df
else:
    df = df[df['Agent'] == select_agent]


if select_topic == 'Select a Topic':
    df = df
else:
    df = df[df['Topic'] == select_topic]


def display_card(title, value):
    st.markdown(
        f"""
        <div style="background-color: #808080;  border-radius: 10px; text-align: center; margin-bottom: 10px;width:200px;">
            <h3 style="margin: 0;font-size: 17px;font-weight: bold;text-align: center; ">{title}</h3>
            <p style="font-size: 15px; font-weight: bold; margin: 0;">{value}</p>
        </div;
        """,
        unsafe_allow_html=True
    )


for idx, row in df.iterrows():
    t = row['Time']
    minute = t.minute
    if minute < 30:
        rounded_minute = 0
    else:
        rounded_minute = 30
    sec = 0
    time = f"{t.hour}:{rounded_minute:02}:{sec}"
    time2 = datetime.strptime(time, '%H:%M:%S').time()
    df.at[idx,'half_hour_time'] = time2


month = df['Date'].dt.strftime('%b')
    

overall_calls = df['Call Id'].count()
overall_calls_answered = df[df['Answered (Y/N)'] == 'Y']
count_overall_calls_answered = overall_calls_answered['Answered (Y/N)'].count()
overall_calls_abandoned = df[df['Answered (Y/N)'] == 'N']
count_overall_calls_abandoned = overall_calls_abandoned['Answered (Y/N)'].count()
average_speed_of_answer = df['Speed of answer in seconds'].mean().round(2)
resolved_calls = df[df['Resolved'] == 'Y']
count_resolved_calls = resolved_calls['Resolved'].count()
unresolved_calls = df[df['Resolved'] == 'N']
count_unresolved_calls = unresolved_calls['Resolved'].count()
count_for_each_rating = df.groupby('Satisfaction rating')['Call Id'].count().reset_index()
count_for_each_rating.columns = ['Satisfaction rating','Count']
count_calls_by_time = df.groupby('half_hour_time')['Call Id'].count().reset_index()
count_calls_by_time.columns = ['Time','Count']
count_calls_by_month = df.groupby(month)['Call Id'].count().reset_index()   
count_calls_by_month.columns = ['Month','Count']


container = st.container()

cols = container.columns(6)

#display_card('Overall Calls Come',overall_calls)
#display_card('Overall Calls Answered',count_overall_calls_answered)
#display_card('Overall Calls Abandoned',count_overall_calls_abandoned)
#display_card('Average Speed of Answer in Seconds',average_speed_of_answer)
#display_card('Resolved Calls',count_resolved_calls)
#display_card('Unresolved Calls',count_unresolved_calls)

cols[0].metric("Overall Calls Come", overall_calls)
cols[1].metric("Overall Calls Answered", count_overall_calls_answered)
cols[2].metric("Overall Calls Abandoned", count_overall_calls_abandoned)
cols[3].metric("Avg Speed of Answer(Sec)", average_speed_of_answer)
cols[4].metric("Resolved Calls", count_resolved_calls)
cols[5].metric("Unresolved Calls", count_unresolved_calls)

fig = px.bar(count_for_each_rating,x='Satisfaction rating',y='Count',title='Overall Customer Satisfaction')
fig.update_layout(width=700, height=400)
fig2 = px.line(count_calls_by_time,x='Time',y='Count',title='Calls By Time')
fig2.update_layout(width=700, height=400)
fig3 = px.bar(count_calls_by_month,x='Month',y='Count',title='Number of Calls Per Month')
fig3.update_layout(width=700, height=400)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig)
   
with col2:
    st.plotly_chart(fig2)

col3,col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3)

avg_rating = df['Satisfaction rating'].mean()

def create_gauge(value, target, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': target, 'increasing': {'color': "RebeccaPurple"}},
        gauge={
            'axis': {'range': [0, 5], 'tickwidth': 1, 'tickcolor': "gray"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': '#87CEEB'}],
            'threshold': {
                'line': {'color': "purple", 'width': 4},
                'thickness': 0.75,
                'value': target}}))
    
    return fig


target_rating = 4.5

fig4 = create_gauge(avg_rating, target_rating, 'Average Satisfaction')

fig4.update_layout(width=700, height=400)

with col4:
    st.plotly_chart(fig4)










