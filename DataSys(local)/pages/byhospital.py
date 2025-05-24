import streamlit as st
import pandas as pd
import plotly.express as pxpress


if 'admissions' not in st.session_state:
    st.session_state.admissions = pd.read_csv('./tables/fact_admissions.csv')

admissions_full = st.session_state.admissions

hospital_list = admissions_full["Hospital"].dropna().unique()
hospital_list.sort()
selected_hospital = st.selectbox("Select a Hospital", options=hospital_list)

admissions = admissions_full[admissions_full["Hospital"] == selected_hospital]

col1, col2, col3 = st.columns(3)
col1.metric('Total Patients', admissions['patient_id'].nunique())
col2.metric('Total Admissions', admissions['admission_id'].nunique())
col3.metric('Average Age', round(admissions['age'].mean(), 2))

col4, col5, col6 = st.columns(3)
col4.metric('Average Length of Stay', round(admissions['length_of_stay'].mean(), 2))
col5.metric('Average LACE Score', round(admissions['lace_score'].mean(), 2))
col6.metric('Average CCI Score', round(admissions['cci_score'].mean(), 2))

admitted_from = admissions.groupby('admission_location')['admission_id'].nunique().reset_index(name='Number of Admissions From Location')
admissions_by_type = admissions.groupby('admission_type')['admission_id'].nunique().reset_index(name='Number of Admissions Per Type')
discharge_locations = admissions.groupby('discharge_location')['admission_id'].nunique().reset_index(name='Number of Admissions Per Discharge Location')

st.subheader("Admissions Overview")
col7, col8, col9 = st.columns(3)

with col7:
    admitted_from_sorted = admitted_from.sort_values("Number of Admissions From Location", ascending=False)
    fig1 = pxpress.bar(
        admitted_from_sorted,
        x='Number of Admissions From Location',
        y='admission_location',
        orientation='h',
        title='Admissions by Location',
        color='admission_location',
        color_discrete_sequence=pxpress.colors.qualitative.Pastel
    )
    fig1.update_layout(yaxis_title="Admission Location", xaxis_title="Admissions", showlegend=False)
    fig1.update_traces(marker_line_width=1.5, marker_line_color='gray', width=0.6)
    st.plotly_chart(fig1, use_container_width=True)

with col8:
    admissions_by_type_sorted = admissions_by_type.sort_values("Number of Admissions Per Type", ascending=False)
    fig2 = pxpress.bar(
        admissions_by_type_sorted,
        x='Number of Admissions Per Type',
        y='admission_type',
        orientation='h',
        title='Admissions by Type',
        color='admission_type',
        color_discrete_sequence=pxpress.colors.qualitative.Pastel
    )
    fig2.update_layout(yaxis_title="Admission Type", xaxis_title="Admissions", showlegend=False)
    fig2.update_traces(marker_line_width=1.5, marker_line_color='gray', width=0.6)
    st.plotly_chart(fig2, use_container_width=True)

with col9:
    discharge_locations_sorted = discharge_locations.sort_values("Number of Admissions Per Discharge Location", ascending=False)
    fig3 = pxpress.bar(
        discharge_locations_sorted,
        x='Number of Admissions Per Discharge Location',
        y='discharge_location',
        orientation='h',
        title='Discharge Locations',
        color='discharge_location',
        color_discrete_sequence=pxpress.colors.qualitative.Pastel
    )
    fig3.update_layout(yaxis_title="Discharge Location", xaxis_title="Admissions", showlegend=False)
    fig3.update_traces(marker_line_width=1.5, marker_line_color='gray', width=0.6)
    st.plotly_chart(fig3, use_container_width=True)

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
