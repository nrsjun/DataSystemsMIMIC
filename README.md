# HeartTrack Clinical Dashboard
This repo contains a Streamlit clinical dashboard using the MIMIC-IV Dataset

---

## Structure
```
HeartTrack/
│
├── local/                     # Please use this folder. 
│   ├── Streamlit/             # USE THIS
│   └── tables/                # DATA 
│
├── cloudver/                  # This has the code for the cloud version. But I have exceeded my free limit and even had to pay extra.
│   └── Streamlit/             # DO NOT USE THIS. BUT FEEL FREE TO EXAMINE THE DIFFRERENCES BETWEEN THE TWO VERSIONS.
│
├── .streamlit/
│   └── secrets.toml           # GCP credentials- this doesn't work since I disabled Google Cloud so I don't get charged. 
│
└── README.md                  # This is the read me file. 
```
---
## How to Ru
1. Use VSCode or open the local folder. The cloud version will not connect to my BigQuery project to avoid charges to my credit card.

2. Install Requirements.txt.
```
pip install -r requirements.txt
```

3. Run the app by using streamlit
```
streamlit run main.py
```


