## Getting google credentials

1.  On google website go to Settings > Service Accounts > Manage Keys > JSON.

2.  save JSON to `.streamlit/sa-key.json`

3.  Copy info into `.streamlit/secrets.toml` and refactor as toml format.


## Set Path

1.  `export GOOGLE_APPLICATION_CREDENTIALS="/Users/junichiocena/Desktop/DataSys/.streamlit/secrets.toml"`


## Run the python
```
> python connecting.py
```



## Run in browser

```
> streamlit run connecting.py
```

