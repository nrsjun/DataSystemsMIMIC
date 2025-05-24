from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Patient List", layout="wide")
st.title("Patient List by Hospital")

# Load credentials from secrets
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)
# Cache the admissions in session_state
if 'admissions' not in st.session_state:
    query = """SELECT * FROM `datasystemsmimic.datasystems_final.admissions_enriched`"""
    st.session_state.admissions = client.query(query).to_dataframe()

admissions = st.session_state.admissions

hospital_list = admissions["Hospital"].dropna().unique()
hospital_list.sort()
selected_hospital = st.selectbox("Select a Hospital", options=hospital_list)

filtered = admissions[admissions["Hospital"] == selected_hospital]

search_query = st.text_input("Search Patients", placeholder="Search by patient ID")


if search_query:
    filtered = filtered[
        filtered["patient_id"].astype(str).str.contains(search_query, case=False, na=False) 
    ]

patient_table = filtered[[
    "patient_id",
    "age",
    "gender",
    "diagnosis_description",
    "length_of_stay",
    "lace_score",
    "cci_score"
]].rename(columns={
    "diagnosis_description": "Reason for Admission",
    "lace_score": "LACE Score",
    "cci_score": "CCI Score"
}).drop_duplicates()

# sort table based on column variables (eg. patient Id, age, gender, lace score, CCI)
sort_columns = list(patient_table.columns)
sort_by = st.selectbox("Sort by", options=sort_columns)
sort_order = st.radio("Sort order", ["Ascending", "Descending"], horizontal=True)
ascending = sort_order == "Ascending"

patient_table["Select"] = False
sorted_patient_table = patient_table.sort_values(by=sort_by, ascending=ascending)
edited_table = st.data_editor(
    sorted_patient_table,
    use_container_width=True,
    num_rows="dynamic",
    disabled=["patient_id", "age", "gender", "Reason for Admission", "LACE Score", "CCI Score"]
)

selected_rows = edited_table[edited_table["Select"] == True]

if len(selected_rows) == 1:
    selected_pid = selected_rows.iloc[0]["patient_id"]
    st.session_state.selected_patient_id = selected_pid
    st.markdown(f"### Selected Patient ID: {selected_pid}")
    if st.button("Go to Patient Chart"):
        st.switch_page("pages/patientchart.py")
elif len(selected_rows) > 1:
    st.warning("Please select only one patient.")
else:
    st.info("Select a patient from the table to view their chart.")