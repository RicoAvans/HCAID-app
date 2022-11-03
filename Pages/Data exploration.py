import streamlit as st
import pandas as pd
import numpy as np
import time
import seaborn as sns

colNames = ['hoeveel', 'wanneer', 'laat', 'lang', 'kwaliteit']
data = pd.read_csv(
    filepath_or_buffer=r'C:\Users\Ricardo\OneDrive - Avans Hogeschool\1 school HBO\School HBO v2\4.1\Human Centered AI Design\web application\Cafeïne en slaaptekort.csv'
    , sep=",", header=0, names=colNames, usecols=[1, 2, 3, 4, 5])

st.write(data)

# sns.heatmap(data)
