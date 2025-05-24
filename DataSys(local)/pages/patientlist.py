import streamlit as st
import pandas as pd

st.set_page_config(page_title="Patient List", layout="wide")
st.title("Patient List by Hospital")

#check if the admissions dataframe is already loaded but if not, load it
if 'admissions' not in st.session_state:
    st.session_state.admissions = pd.read_csv('./tables/fact_admissions.csv')

admissions = st.session_state.admissions

hospital_list = admissions["Hospital"].dropna().unique()
hospital_list.sort()
selected_hospital = st.selectbox("Select a Hospital", options=hospital_list)

filtered = admissions[admissions["Hospital"] == selected_hospital]

search_query = st.text_input("Search Patients", placeholder="Search by patient ID")

#search box for patient ID
if search_query:
    filtered = filtered[
        filtered["patient_id"].astype(str).str.contains(search_query, case=False, na=False) 
    ]

#display the filtered patient list
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


#use 
patient_table["Select"] = False
edited_table = st.data_editor(
    patient_table,
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