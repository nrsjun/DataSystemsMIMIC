# streamlit_app.py

import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery
from google.oauth2 import service_account

#config 
st.set_page_config(page_title="HeartTrack Dashboard", layout="wide")

# Connect to BigQuery
sa_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(sa_info)
client = bigquery.Client(credentials=credentials, project=sa_info["project_id"])

# load the fact tables
@st.cache_data(ttl=3600)
def load_admissions():
    """Load latest admission record per patient"""
    query = """
    SELECT AS VALUE
      ARRAY_AGG(adm ORDER BY adm.admittime DESC LIMIT 1)[OFFSET(0)]
    FROM `datasystemsmimic.datasystems_final.admissions_enriched` adm
    GROUP BY adm.patient_id
    """
    return client.query(query).to_dataframe()

# Pages
def show_dashboard():
    st.title("HeartTrack Dashboard")
    st.markdown("### Key admission insights")

    # 1) Load admissions 
    df = load_admissions()

    # 2) Display Key Metrics
    st.markdown("**Key Metrics**")
    with st.container():
        c1, c2, c3 = st.columns(3)

        # get average LACE and CCI scores
        avg_lace = df.lace_score.mean()
        avg_cci  = df.cci_score.mean()

        # first row of metrics
        c1.metric("Total Patients", df.patient_id.nunique())
        c2.metric("Total Admissions", df.shape[0])
        c3.metric("Avg. Length of Stay (days)", round(df.length_of_stay.mean(), 2))

        # second row
        c1.metric("Average Age", round(df.age.mean(), 2))
        c2.metric("Average LACE Score", f"{avg_lace:.1f}")
        c3.metric("Average CCI Score",  f"{avg_cci:.1f}")

        # captions under LACE and CCI
        c2.caption(
            f"Mean LACE = {avg_lace:.1f} → " +
            ("High risk" if avg_lace > 9 else "Moderate risk" if avg_lace > 4 else "Low risk")
        )
        c3.caption(
            f"Mean CCI = {avg_cci:.1f} → " +
            ("High comorbidity" if avg_cci > 5 else "Moderate comorbidity" if avg_cci > 2 else "Low comorbidity")
        )

    #3) Display Demographics
    st.markdown("**Demographics**")
    with st.container():
        c1, c2 = st.columns(2)
       # Age distribution histogram
        age_hist = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("age:Q", bin=alt.Bin(maxbins=20), title="Age"),
                y=alt.Y("count():Q", title="Number of Patients"),
                color=alt.Color("age:Q", bin=alt.Bin(maxbins=20), legend=None),
                tooltip=[alt.Tooltip("count():Q", title="Count")]
            )
            .properties(title="Age Distribution")
        )

        c1.altair_chart(age_hist, use_container_width=True)




    

def show_patient_list():
    """Page for searching and listing patients."""
    st.title("Patient List")
    df = load_admissions()

    # Search box
    search = st.text_input("Search Patient ID")
    if search:
        df = df[df.patient_id.astype(str).str.contains(search)]

    # Quick filters
    st.markdown("**Quick Filters:**")
    c1, c2, c3 = st.columns(3)
    lace_f = c1.checkbox("High LACE (>9)")
    cci_f = c2.checkbox("High CCI (>2)")
    los_f = c3.checkbox("Long LOS (>7d)")

    if lace_f and "lace_score" in df.columns:
        df = df[df.lace_score > 9]
    if cci_f and "cci_score" in df.columns:
        df = df[df.cci_score > 2]
    if los_f and "length_of_stay" in df.columns:
        df = df[df.length_of_stay > 7]

    # Display table
    display_cols = [
        "patient_id", "age", "gender", "admission_type",
        "length_of_stay", "diagnosis_description", "cci_score", "lace_score"
    ]
    display_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(df[display_cols], use_container_width=True)

    # Optional selection (for future drill-down)
    if df.patient_id.tolist():
        st.selectbox("Select Patient ID (drill-down coming soon)", df.patient_id.tolist())
    else:
        st.info("No patients match your filters.")


# --- App layout ---
def main():
    pages = {"Home": show_dashboard, "Patients": show_patient_list}
    choice = st.sidebar.radio("Go to", list(pages.keys()))
    pages[choice]()


if __name__ == "__main__":
    main()
