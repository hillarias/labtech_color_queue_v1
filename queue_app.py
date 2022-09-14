# streamlit_app.py

import streamlit as st
from gsheetsdb import connect

st.set_page_config(layout="wide")

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


in_prog = []
completed = []

# Print results.
for row in rows:
    
    curr = row.FORMULATION + " submitted by " + row.PERSON
    if (row.COMPLETE == 'NO'): 
        in_prog.append(curr)
    else: 
        completed.append(curr)

prog_header  = '<p style="font-family:Arial; color:Blue; font-size: 20px;">In Progress</p>'
st.markdown(prog_header, unsafe_allow_html=True)
for entry in in_prog:
    st.write(entry)

completed_header = '<p style="font-family:Arial; color:Red; font-size: 20px;">Completed</p>'
st.subheader(completed_header, unsafe_allow_html = True)
for entry in completed:
    st.write(entry)



        

    
