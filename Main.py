# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:45:19 2026

@author: monka
"""  
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import numpy as np 
import io
import webbrowser
import gdown

    
st.set_page_config(layout="wide")
@st.cache_data
@st.cache_data(ttl=1, show_spinner=False)
@st.cache_data(show_spinner=False)
def load_my_data():

    filename_0 = "Baza_Danych_FULL_names.pkl" 
    file_id0 = '1OB7gvnArcyFuUPmpj3Qa1pOvnLe70j19'

    def download_file(file_id, output_name):
        url = f'https://drive.google.com/uc?id={file_id}'
        
        if os.path.exists(output_name):
            os.remove(output_name)
        try:
            # 
            gdown.download(url, output_name, quiet=False)
        except Exception as e:
            st.error(f"Błąd pobierania {output_name}: {e}")

        
    with st.spinner('Synchronizacja z Google Drive...'):
        download_file(file_id0, filename_0)
    try:
        data_0 = pd.read_pickle(filename_0)
        return data_0
    except Exception as e:
        st.error(f"Błąd wczytywania pkl: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Wywołanie danych
df= load_my_data()


#%%---------------------------------------------------------------------------------------Title--------------------------------------------------------------------------------------------------------------------------------
kolor_ramki = "#ff9300"  # Twój kolor (np. niebieski)
kolor_tla = "#363636"    # Jasny odcień dla wypełnienia
pomarancz = "#ff9300"
bg_color="#363636"

st.subheader("Baza danych")
st.dataframe(df,height=400,use_container_width=True)


                
