import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

client = bigquery.Client()

# patient_name = st.sidebar.text_input('Patient name')
# patient_number = st.sidebar.text_input('Patient number', type='password')

state_name = st.sidebar.text_input('US state:')

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

sql = f"""
SELECT subpopulation, avg(value) as avg_value FROM `bigquery-public-data.america_health_rankings.ahr` where
lower(state_name) = "{state_name.lower()}"
group by 1
having subpopulation is not null"""

    
if st.button("Process"):
    
    rows = run_query(sql)
     
    st.write(sql)
    # Print results.
    st.write("Results:")
    for row in rows:
        st.write(row['subpopulation'] + "✍️ " + str(row['avg_value']))