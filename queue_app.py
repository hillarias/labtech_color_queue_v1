# streamlit_app.py

import streamlit as st
from gsheetsdb import connect
import plotly
import plotly.express as px
import pandas as pd
from datetime import datetime
from datetime import date

st.set_page_config(layout="wide")
st.image('https://i.pinimg.com/originals/0a/2d/2c/0a2d2c61d0c678404f26a332ed015c38.png')

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

st.image('https://ginsbergs.com/wp-content/uploads/2021/08/Beyond-Meat-Logo.png', width=300)
st.header('Color Team Formulation Queue')

received = []
in_prog = []
completed = ["","","","","","","","","","","",""]
rec_index = 1

# Print results.
for row in rows:
    
    curr = row.FORMULATION + " submitted by " + row.PERSON_SUBMITTED
    
    if row.IN_PROGRESS == 'NO':
        curr = str(rec_index) + ") " + row.FORMULATION + " submitted by " + row.PERSON_SUBMITTED 
        rec_index += 1
        received.append(curr)
    
    
        
    elif row.COMPLETE == 'NO': 
        curr =  row.FORMULATION + " submitted by " + row.PERSON_SUBMITTED + ' - ' + row.LAB_TECH
        
        in_prog.append(curr)
    else: 
        curr =  row.FORMULATION + " submitted by " + row.PERSON_SUBMITTED + ' - ' + row.LAB_TECH
        completed.append(curr)

        
col1, col2, col3 = st.columns(3)

with col1:
    
    rec_header  = '<p style="font-family:helvetica; color: indianred;; font-size: 30px;"><u>Received</u></p>'
    st.markdown(rec_header, unsafe_allow_html=True)
    for entry in received:
        st.write(entry)

with col2:
    prog_header  = '<p style="font-family:helvetica; color:darkolivegreen; font-size:30px;"><u>In Progress</u></p>'
    st.markdown(prog_header, unsafe_allow_html=True)
    for entry in in_prog:
        st.write(entry)
   

with col3:
    comp_header = '<p style="font-family:helvetica; color:royalblue; font-size: 30px;"><u>Completed</u></p>'
    st.markdown(comp_header, unsafe_allow_html = True)
    counter = -1
    for entry in range(10):
        st.write(completed[counter])
        counter -= 1

           
        
        
name_count = {}
for row in rows:
    if row.PERSON_SUBMITTED in name_count.keys():
        name_count[row.PERSON_SUBMITTED] += 1
    else:
        name_count[row.PERSON_SUBMITTED]= 1

exp_count = pd.DataFrame(name_count.items(), columns=['Name', 'Exp_Count'])

exp_chart = px.bar(exp_count, x = 'Name', y = 'Exp_Count', color = "Exp_Count", color_continuous_scale= 'Agsunset')
exp_chart.update_layout(width= 800,height = 500)
exp_chart.update_layout(title='Experiment Count', title_x=0.45,
                       legend_font_size=15)

st.write('##')
st.write('##')
st.write('##')

queue_check = st.checkbox('Check here for queue summary data')
if queue_check:
    st.header('Experiment Submission Count by Team Member')
    st.write(exp_chart)

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def days_between_v2(d1, d2):
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

    
tech_month_count = {}
for row in rows:
    if days_between(str(date.today()),str(row.DATE_COMPLETED)) <= 30:
            if row.LAB_TECH in name_count.keys():
                tech_month_count[row.LAB_TECH] += 1
            else:
                tech_month_count[row.LAB_TECH]= 1
        
            if tech_month_count.in('EH/MH'):
                tech_month_count['Emily'] += tech_month_count['EH/MH']
                tech_month_count['Mala'] += tech_month_count['EH/MH']
            
            if tech_month_count.in('EH/AA'):
                tech_month_count['Emily'] += tech_month_count['EH/AA']
                tech_month_count['Alexis'] += tech_month_count['EH/AA']
                
            if tech_month_count.in('AA/MH'):
                tech_month_count['Alexis'] += tech_month_count['AA/MH']
                tech_month_count['Mala'] += tech_month_count['AA/MH']
            
            if tech_month_count.in('All'):
                tech_month_count['Emily'] += tech_month_count['All']
                tech_month_count['Mala'] += tech_month_count['All']
                tech_month_count['Alexis'] += tech_month_count['All']
        
        
            
month_count = pd.DataFrame(tech_month_count.items(), columns=['Name', 'Monthly_Exp_Count'])
cleaned_month = month_count[(month_count['Name'] == 'Emily') or (month_count['Name'] == 'Alexis') or (month_count['Name'] == 'Mala')]
    
month_exp_chart = px.bar(cleaned_month, x = 'Name', y = 'Exp_Count', color = "Exp_Count", color_continuous_scale= 'Agsunset')
month_exp_chart.update_layout(width= 800,height = 500)
month_exp_chart.update_layout(title='Monthly Experiment Count', title_x=0.45,
                       legend_font_size=15)
    

month_check = st.checkbox('Check here for monthly experiment statistics')
if month_check:
    st.write(month_exp_chart)






turnover_check = st.checkbox('Check here for experiment turnover statistics')
if turnover_check:
    turnover_count =  0 
    exp_count = 0
    for row in rows:
        if row.COMPLETE == 'YES':
            temp_turnover = days_between(str(row.DATE_RECEIVED),str(row.DATE_COMPLETED))
            turnover_count+= temp_turnover
            exp_count += 1
            
    st.subheader('Number of Experiements Batched: '+ '       ' + str(exp_count))
    st.subheader('Average Turnover Once Received:'+ '       '+ str(turnover_count/exp_count)+' Days')
        
            
    
    
    
    
    
    
