import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="BTF Vitals View", layout="wide")

# Check if patient is selected
if 'selected_patient_id' not in st.session_state:
    st.error("No patient selected.")
    st.stop()

pid = st.session_state.selected_patient_id
st.title(f"Patient Chart for: {pid}")

#  Close button to return to patient list
if st.button("Return to Patient List"):
    st.switch_page("pages/patientlist.py")

# Load data
vitals = pd.read_csv('./tables/fact_vitals.csv')
labs = pd.read_csv('./tables/fact_lab_results.csv')

#only load the data for the selected patient
vitals = vitals[vitals["patient_id"] == pid]
labs = labs[labs["patient_id"] == pid]

#get the latest (10) vitals and labs 
latest_vitals_df = (
    vitals.sort_values("vital_time", ascending=False)
    .groupby("vital_name")
    .head(10)
    .sort_values(["vital_name", "vital_time"], ascending=[True, False])
)

latest_labs_df = (
    labs.sort_values("lab_time", ascending=False)
    .groupby("lab_type_name")
    .head(10)
    .sort_values(["lab_type_name", "lab_time"], ascending=[True, False])
)


#visualse the vitals
def plot_vitals(vitals_df):
    fig = go.Figure()
    for vital_name in vitals_df["vital_name"].unique():
        df = vitals_df[vitals_df["vital_name"] == vital_name]
        fig.add_trace(go.Scatter(
            x=df["vital_time"],
            y=df["vital_reading"],
            mode='lines+markers',
            name=vital_name
        ))
    fig.update_layout(title="Vitals Over Time", xaxis_title="Time", yaxis_title="Value")
    return fig

#visualse the labs
def plot_labs(labs_df):
    fig = go.Figure()
    for lab_type_name in labs_df["lab_type_name"].unique():
        df = labs_df[labs_df["lab_type_name"] == lab_type_name]
        fig.add_trace(go.Scatter(
            x=df["lab_time"],
            y=df["lab_value"],
            mode='lines+markers',
            name=lab_type_name
        ))
    fig.update_layout(title="Labs Over Time", xaxis_title="Time", yaxis_title="Value")
    return fig

if latest_vitals_df.empty:
    st.warning("No vital signs available for this patient.")

# display vitals in 2 columns
st.subheader("Vitals")
vital_cols = st.columns(2)
ordered_vitals = ["SBP", "Heart Rate", "DBP", "SpO2"]
vital_colors = {
    "SBP": "red",
    "DBP": "red",
    "SpO2": "blue",
    "Heart Rate": "green"
}
for i, vital_name in enumerate(ordered_vitals):
    df = latest_vitals_df[latest_vitals_df["vital_name"] == vital_name]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["vital_time"],
        y=df["vital_reading"],
        mode='lines+markers',
        name=vital_name,
        line=dict(color=vital_colors.get(vital_name, 'gray')),
        marker=dict(color=vital_colors.get(vital_name, 'gray'), size=10)
    ))
    fig.update_layout(title=f"{vital_name} Over Time", xaxis_title="Time", yaxis_title="Result")
    vital_cols[i % 2].plotly_chart(fig, use_container_width=True)

# display labs in 4 columns
st.subheader("Labs")
lab_cols = st.columns(3)
# Color mapping for labs (high-contrast for grey/white background)
lab_colors = {
    "Creatinine": "#0044cc",     # vivid blue
    "Hemoglobin": "#cc0000",     # deep red
    "Magnesium": "#7e00cc",      # dark purple
    "NT-proBNP": "#ff6600",      # bright orange
    "Potassium": "#007a29",      # deep green
    "Sodium": "#008080",         # dark teal
    "Troponin T": "#ffcc00",     # golden yellow
    "eGFR": "#5c4033"            # dark brown
}
for i, lab_type_name in enumerate(latest_labs_df["lab_type_name"].unique()):
    df = latest_labs_df[latest_labs_df["lab_type_name"] == lab_type_name]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["lab_time"],
        y=df["lab_value"],
        mode='lines+markers',
        name=lab_type_name,
        line=dict(color=lab_colors.get(lab_type_name, 'gray')),
        marker=dict(color=lab_colors.get(lab_type_name, 'gray'), size=10),
        

    ))
    fig.update_layout(title=f"{lab_type_name} Over Time", xaxis_title="Time", yaxis_title="Result")
    lab_cols[i % 3].plotly_chart(fig, use_container_width=True)
