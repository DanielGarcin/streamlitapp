import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile
import os

# Configuration de la page
st.set_page_config(page_title="Analyse des comportements d'achat avec DuckDB", layout="wide")

# Titre de l'application
st.title("Analyse des comportements d'achat avec DuckDB et Streamlit")
st.write("Cette application analyse les données de comportement d'achat en utilisant DuckDB et Streamlit.")