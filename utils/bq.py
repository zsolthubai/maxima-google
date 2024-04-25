from google.cloud import bigquery
import datetime

client = bigquery.Client()

def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

def get_patient_diagnosis(patient_id):
    
    sql = f"""SELECT cancer_detected_in, descriptive_diagnosis_field, type_of_cancer FROM `qwiklabs-gcp-04-b01a5678dcab.patient_data.p_diagnosis_n`
    WHERE patient_id = {patient_id} """
    
    rows = run_query(sql)
    
    for row in rows:
        d = {"cancer_detected_in": row['cancer_detected_in'], "descriptive_diagnosis_field": row['descriptive_diagnosis_field'], "type_of_cancer": row['type_of_cancer']}
    return d
    
def get_patient_info(patient_id):
    sql = f"""SELECT gender, year_of_birth, first_name, last_name FROM `qwiklabs-gcp-04-b01a5678dcab.patient_data.p_contact_n`
    WHERE patient_id = {patient_id} """
    
    rows = run_query(sql)
    
    for row in rows:
        d = {"gender": row['gender'], "year_of_birth": row['year_of_birth'], "first_name": row['first_name'], "last_name": row['last_name']}
    return d
    
def get_patient_id(patient_name):
    sql = f"""
    SELECT patient_id FROM `qwiklabs-gcp-04-b01a5678dcab.patient_data.p_contact_n`
    WHERE REGEXP_CONTAINS(CONCAT(first_name," ", last_name), "{patient_name}")"""
    
    rows = run_query(sql)
    for row in rows:
        return row["patient_id"]
    
def get_patient_treatment(patient_id):
    sql = f"""SELECT descriptive_treatment_field, side_effects, start_date_of_treatment
     FROM `qwiklabs-gcp-04-b01a5678dcab.patient_data.p_treatment_n`
     WHERE patient_id = {patient_id} """
     
    rows = run_query(sql)
    for row in rows:
        d = {"descriptive_treatment_field": row['descriptive_treatment_field'], "side_effects": row['side_effects'], "start_date_of_treatment": row['start_date_of_treatment']}
        
    return d

def get_patient_records(patient_id=None, patient_name=None):
    
    if not patient_id:
        patient_id = get_patient_id(patient_name)
    
    info = get_patient_info(patient_id)
    diagnosis = get_patient_diagnosis(patient_id)
    treatment = get_patient_treatment(patient_id)
    
    return_string = f"""
    The following patient data is provided:
    
    Name: {info["first_name"]}
    
    Last name: {info["last_name"]}
    
    Gender: {info["gender"]}
    
    Age: {int(datetime.date.today().year)-int(info["year_of_birth"])}
    
    Cancer Type: {diagnosis["type_of_cancer"]}
    
    Cancer detected in: {diagnosis["cancer_detected_in"]}
    
    Descriptive Diagnosis: {diagnosis["descriptive_diagnosis_field"]}
    
    Descriptive Treatment: {treatment["descriptive_treatment_field"]}
    
    Side effects: {treatment["side_effects"]}
    
    Treatment start date: {datetime.date.today()-treatment["start_date_of_treatment"]} ago
    """
    return return_string

# state_name = st.sidebar.text_input('Patient ID:')

# # Perform query.
# # Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def run_query(query):
#     query_job = client.query(query)
#     rows_raw = query_job.result()
#     # Convert to list of dicts. Required for st.cache_data to hash the return value.
#     rows = [dict(row) for row in rows_raw]
#     return rows

# sql = f"""
# SELECT subpopulation, avg(value) as avg_value FROM `bigquery-public-data.america_health_rankings.ahr` where
# lower(state_name) = "{state_name.lower()}"
# group by 1
# having subpopulation is not null"""

    
# if st.button("Process"):
    
#     rows = run_query(sql)
     
#     st.write(sql)
#     # Print results.
#     st.write("Results:")
#     for row in rows:
#         st.write(row['subpopulation'] + "✍️ " + str(row['avg_value'])) 