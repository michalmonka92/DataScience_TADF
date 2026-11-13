# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:45:19 2026

@author: monka
"""  
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import numpy as np 
import io
import webbrowser

from rdkit import Chem
from rdkit.Chem import Descriptors, rdDetermineBonds, Draw
import subprocess
from rdkit.Chem import rdmolfiles  
import py3Dmol
from rdkit.Chem import rdMolAlign
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D

import shutil
import re
from natsort import natsorted
from io import BytesIO
from PIL import Image

import streamlit.components.v1 as components


import gdown




        
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', str(s))]
    
st.set_page_config(layout="wide")
@st.cache_data
@st.cache_data(ttl=1, show_spinner=False)
@st.cache_data(show_spinner=False)
def load_my_data():



    filename_0 = "Baza_Danych_FULL_names.pkl" 
    file_id0 = '1OB7gvnArcyFuUPmpj3Qa1pOvnLe70j19'
        


    # Funkcja pomocnicza do pobierania
    def download_file(file_id, output_name):
        url = f'https://drive.google.com/uc?id={file_id}'
        
        if os.path.exists(output_name):
            os.remove(output_name)
        
        try:
            # 
            gdown.download(url, output_name, quiet=False)
        except Exception as e:
            st.error(f"Błąd pobierania {output_name}: {e}")

    # Pobieranie plików
    with st.spinner('Synchronizacja z Google Drive...'):
        download_file(file_id0, filename_0)


    # Wczytywanie
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

st.markdown("""<style>
    /* Celujemy w tekst nagłówka expandera */
    .stExpander details summary p {
        color: cyan !important;
        font-weight: bold;
        font-size: 1.1rem;}
    </style>
    """, unsafe_allow_html=True)
st.markdown(f"""<hr style="height:5px;margin-top: -1px; border:none; color:{kolor_tla}; background-color:{kolor_tla};" />""", unsafe_allow_html=True)   
st.markdown(f"""
        <style>
        .moja-ramka1 {{ 
        border-radius: 14px;
        padding: 25px;
        background-color: {kolor_tla};
        color=#ffffff;
        text-align: center;
        height: 90px;
    }}
    .moja-ramka1 h4 {{
        color: "#ffffff";
        font-size: 18px;
        margin: -5px;
    }}
    </style>
    
    <div class="moja-ramka1">
        <h4>TADF dataset for Machine Learning</h4>
    </div>
    """, unsafe_allow_html=True) 
st.markdown(" ") # Bardzo mały odstęp
cola,colb=st.columns([4.7,5])
with cola:
           

        st.markdown(f"""
        <style>
        .moja-ramka {{ 
        border-radius: 10px;
        padding: 30px;
        background-color: {kolor_tla};
        text-align: center;
        height: 40px;
    }}
    .moja-ramka h4 {{
        color: {kolor_ramki};
        font-size: 18px;
        margin: 15px;
    }}
    </style>
    
    <div class="moja-ramka">
        <h4>Linker modifications</h4>
    </div>
    """, unsafe_allow_html=True)  
        st.markdown(f"""<hr style="height:5px;margin-top: -3px; border:none; color:{pomarancz}; background-color:{pomarancz};" />""", unsafe_allow_html=True)
        image = Image.open('linkers.jpg')
        st.image(image, use_container_width=True)     

with colb:
        st.markdown(f"""
        <style>
        .moja-ramka {{ 
        border-radius: 10px;
        padding: 0px;
        background-color: {kolor_tla};
        text-align: center;
        height: 40px;
    }}
    .moja-ramka h4 {{
        color: {kolor_ramki};
        font-size: 18px;
        margin: 0;
    }}
    </style>
    
    <div class="moja-ramka">
        <h4>Substituents</h4>
    </div>
    """, unsafe_allow_html=True)
        st.markdown(f"""<hr style="height:5px;margin-top: -3px; border:none; color:{pomarancz}; background-color:{pomarancz};" />""", unsafe_allow_html=True)

        image = Image.open('Subs.jpg')
        st.image(image, use_container_width=True)      


#%%-------------------------------------------------------------------------------------------------INPUT DATAFRAME STARTING STRUCTURES----------------------------------------------------------------------------------

st.markdown("""<hr style="height:5px; border:none; color:#444444; background-color:#444444;" />""", unsafe_allow_html=True)      
with st.expander("Input DataFrame: Starting Structures (from Dejan) ", expanded=False):
        cola,colb=st.columns([3,8])
        with cola:
                st.markdown('<span style="color: #ff9300; font-weight: bold;">Input DataFrame</span>', unsafe_allow_html=True)
                st.dataframe(df0)

  
                                

        
        with colb:
                st.markdown('<span style="color: #ff9300; font-weight: bold;">Description and Summary</span>', unsafe_allow_html=True)
                st.text("""
This dataset contains starting structures (pre-optimized) of TADF emitters. All data points are aggregated into the `Starting_Structures.pkl` dataframe, which you can download as csv or pkl. 
""")
                stats = df0.describe()
                stats=stats.drop(['top','freq'], axis=0)

                stats_ = stats.style.set_table_styles([
                    {'selector': 'th',
                     'props': [
                     ('background-color', '#ff9300'), # Ciemne tło nagłówka
                     ('color', 'black'),             # POMARAŃCZOWY KOLOR CZCIONKI
                     ('font-family', 'cambria'),
                     ('font-weight', 'bold'),
                     ('border', '1px solid #363636'),
                     ('font-size', '14px')
                     ]
                    }
                ])
                st.table(stats_)

                
