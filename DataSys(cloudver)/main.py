import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as pxpress
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from google.cloud import bigquery
from google.oauth2 import service_account


st.set_page_config(
    page_title="Total Admissions", layout='wide')
st.title('Heart Failure Admissions Dashboard')

if 'admissions' not in st.session_state:
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    st.session_state.admissions = client.query("""
        SELECT * FROM `datasystemsmimic.datasystems_final.admissions_enriched`
    """).to_dataframe()

    st.session_state.vitals = client.query("""
        SELECT * FROM `datasystemsmimic.datasystems_final.fact_vitals`
    """).to_dataframe()

    st.session_state.labs = client.query("""
        SELECT * FROM `datasystemsmimic.datasystems_final.fact_lab_results`
    """).to_dataframe()


# Access cached data
admissions = st.session_state.admissions


    
#show key metrics
col1, col2, col3 = st.columns(3)
col1.metric('Total Patients', admissions['patient_id'].nunique())
col2.metric('Total Admissions', admissions['admission_id'].nunique())
col3.metric('Average Age', admissions['age'].mean().round(2))


#another subcolumn with key metrics
col4, col5, col6 = st.columns(3)
col4.metric('Average Length of Stay', admissions['length_of_stay'].mean().round(2))
col5.metric('Average LACE Score', admissions['lace_score'].mean().round(2))
col6.metric('Averange CCI Score', admissions['cci_score'].mean().round(2))


# get admissions by hospital
admissions_by_hospital = (
    admissions.groupby('Hospital')['admission_id']
    .nunique()
    .reset_index(name='Number of Admissions Per Hospital')
)

# admissions by admission location
admitted_from = (
    admissions.groupby('admission_location')['admission_id']
    .nunique()
    .reset_index(name='Number of Admissions From Location')
)

#admission by type 
admissions_by_type = (
    admissions.groupby('admission_type')['admission_id']
    .nunique()
    .reset_index(name='Number of Admissions Per Type')
)

#discharge locations
discharge_locations = (
    admissions.groupby('discharge_location')['admission_id']
    .nunique()
    .reset_index(name='Number of Admissions Per Discharge Location')
)


# subheader
st.subheader("Admissions by Hospital")
#  2 columns for charts
col7, col8 = st.columns(2)

# admissions by hospital bar chart
with col7:
    admissions_by_hospital_sorted = admissions_by_hospital.sort_values("Number of Admissions Per Hospital", ascending=False)

    hospital_chart = pxpress.bar(
        admissions_by_hospital_sorted,
        x='Number of Admissions Per Hospital',
        y='Hospital',
        orientation='h',
        title='Number of Admissions by Hospital',
        color='Hospital',
        color_discrete_sequence=pxpress.colors.qualitative.Pastel
    )
    hospital_chart.update_layout(
        yaxis_title="Hospital",
        xaxis_title="Number of Admissions",
        showlegend=False,
        height=400,
        barmode='relative'
    )
    hospital_chart.update_traces(width=0.8)
    st.plotly_chart(hospital_chart, use_container_width=True)

# admissions by location bar chart
with col8:
    admitted_from_sorted = admitted_from.sort_values("Number of Admissions From Location", ascending=False)

    location_chart = pxpress.bar(
        admitted_from_sorted,
        x='Number of Admissions From Location',
        y='admission_location',
        orientation='h',
        title='Admissions by Location',
        color='admission_location',
        color_discrete_sequence=pxpress.colors.qualitative.Pastel
    )
    location_chart.update_layout(
        yaxis_title="Admission Location",
        xaxis_title="Number of Admissions",
        showlegend=False,
        height=400,
        barmode='relative'
    )
    location_chart.update_traces(width=0.8)
    st.plotly_chart(location_chart, use_container_width=True)

# admissions by type bar chart
st.subheader("Admissions by Type")
col9, col10 = st.columns(2)
with col9:
    admissions_by_type_sorted = admissions_by_type.sort_values("Number of Admissions Per Type", ascending=False)

    type_chart = pxpress.bar(
        admissions_by_type_sorted,
        x='Number of Admissions Per Type',
        y='admission_type',
        orientation='h',
        title='Admissions by Type',
        color='admission_type',
        color_discrete_sequence=pxpress.colors.qualitative.Pastel
    )
    type_chart.update_layout(
        yaxis_title="Admission Type",
        xaxis_title="Number of Admissions",
        showlegend=False,
        height=400,
        barmode='relative'
    )
    type_chart.update_traces(width=0.8)
    st.plotly_chart(type_chart, use_container_width=True)

# discharge locations bar chart
with col10:
    discharge_locations_sorted = discharge_locations.sort_values("Number of Admissions Per Discharge Location", ascending=False)

    discharge_chart = pxpress.bar(
        discharge_locations_sorted,
        x='Number of Admissions Per Discharge Location',
        y='discharge_location',
        orientation='h',
        title='Discharge Locations',
        color='discharge_location',
        color_discrete_sequence=pxpress.colors.qualitative.Pastel
    )
    discharge_chart.update_layout(
        yaxis_title="Discharge Location",
        xaxis_title="Number of Admissions",
        showlegend=False,
        height=400,
        barmode='relative'
    )
    discharge_chart.update_traces(width=0.8)
    st.plotly_chart(discharge_chart, use_container_width=True)




#create demongraphcs
pt_by_gender = (
    admissions.replace({'gender': {'M': 'Male', 'F': 'Female'}})
    .groupby('gender')['patient_id']
    .nunique()
    .reset_index(name='Number of Patients')
    .rename(columns={'gender': 'Gender'})
)

pt_by_age_group = (
    admissions.assign(
        age_group=pd.cut(
            admissions["age"],
            bins=[0, 20, 40, 60, 80, 100],
            labels=["<20", "21–40", "41–60", "61–80", "81–100"],
            right=False
        )
    )
    .groupby("age_group")["patient_id"]
    .nunique()
    .reset_index(name="Number of Patients")
    .rename(columns={"age_group": "Age Group"})
)

#Need to group the races because tehre are too many categories
admissions['race_grouped'] = 'Other'

admissions.loc[admissions['race'].str.contains('WHITE', case=False, na=False), 'race_grouped'] = 'White'
admissions.loc[admissions['race'].str.contains('BLACK', case=False, na=False), 'race_grouped'] = 'Black'
admissions.loc[admissions['race'].str.contains('ASIAN', case=False, na=False), 'race_grouped'] = 'Asian'
admissions.loc[admissions['race'].str.contains('HISPANIC', case=False, na=False), 'race_grouped'] = 'Hispanic'
admissions.loc[admissions['race'].str.contains('UNKNOWN|UNABLE', case=False, na=False), 'race_grouped'] = 'Unknown'

pt_by_race = (
    admissions.groupby('race_grouped')['patient_id']
    .nunique()
    .reset_index(name='Number of Patients')
    .rename(columns={'race_grouped': 'Race'})
)


#visualise patient demographics
st.subheader("Patient Demographics")

# Create 2 columns for charts
col11, col12, col13= st.columns(3)

# gender pie chart
with col11:
    gender_chart = pxpress.pie(
        pt_by_gender,
        names='Gender',
        values='Number of Patients',
        color='Gender',
        title='Number of Patients by Gender',
        color_discrete_map={'Male': 'lightblue', 'Female': 'lightpink'},
        hole=0.5
    )
    st.plotly_chart(gender_chart, use_container_width=True)

# age chart
with col12:
    age_chart = pxpress.bar(
        pt_by_age_group,
        x="Age Group", 
        y="Number of Patients",
        labels={'Age Group': 'Age Group (Years)'},
        title="Number of Patients by Age Group",
        color="Age Group",
        color_discrete_sequence=pxpress.colors.qualitative.Pastel
    )
    age_chart.update_traces(width=1)
    st.plotly_chart(age_chart, use_container_width=True)


#race chart
with col13:
    race_chart = pxpress.pie(
        pt_by_race,
        names='Race',
        values='Number of Patients',
        title='Number of Patients by Ethnicity',
        color='Race',
        color_discrete_sequence=pxpress.colors.qualitative.Pastel,
        hole=0.3
    )
    st.plotly_chart(race_chart, use_container_width=True)