# HeartTrack Clinical Dashboard
This repo contains a Streamlit clinical dashboard using the MIMIC-IV Dataset

---

## Structure
```
HeartTrack/
├── local/                        # PLEASE USE THIS, THE CLOUD VERSION WILL NOT WORK. SEE REPORT AS TO WHY
│   ├── app.py
│   ├── hash.py
│   ├── main.py
│   ├── README.md
│   ├── requirements.txt
│   ├── credentials.yaml          # (Optional) For login functionality (not implemented)
│   ├── tables/                   # Local data (mimics BigQuery tables)
│   │   ├── fact_admissions.csv
│   │   ├── fact_vitals.csv
│   │   └── fact_lab_results.csv
│   └── pages/                    # Streamlit pages
│       ├── byhospital.py
│       ├── patientchart.py
│       └── patientlist.py
│
├── cloudver/                    # DO NOT USE THE CLOUD VERSION TO RUN THE APP. YOU CAN CHECK THE CODE TO SEE HOW BIG QUERY WAS IMPLEMENTED
│   ├── app.py                   # BUT THE CLOUD VERSION WILL NOT LOAD THE DATA DUE TO CLOUD COSTS.
│   ├── hash.py
│   ├── main.py
│   ├── quick_test.py
│   ├── show_yaml.py
│   ├── eda.ipynb
│   ├── requirements.txt
│   ├── README.md
│   ├── credentials.yaml
│   └── pages/
│       ├── byhospital.py
│       ├── patientchart.py
│       └── patientlist.py
│
├── .streamlit/
│   ├── secrets.toml             
│   └── config.toml              # Optional Streamlit config (theme/title/etc)
│
└── README.md                    # General overview of both versions

```
---
## How to Run
1. Use VSCode or open the local folder. The cloud version will not connect to my BigQuery project to avoid charges to my credit card.

2. Set up virtual environment and Install Requirements.txt.
```
pip install -r requirements.txt
```

3. Run the app by using streamlit
```
streamlit run main.py
```


