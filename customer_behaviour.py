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


# Fonction pour charger les données de démonstration de comprtement d'achat
def charger_donnees_comportement_achat():
    # URL des données de comportement d'achat
    url = "https://www.kaggle.com/datasets/ayeshasiddiqa123/customer-shopping-behavior-dataset"
    return pd.read_csv(url)

# Sidebar pour le chargement des données
st.sidebar.title("Source de données")
source_option = st.sidebar.radio(
    "Choisir la source de données:",
    ["Données Titanic de démonstration", "Télécharger un fichier CSV"]
)
