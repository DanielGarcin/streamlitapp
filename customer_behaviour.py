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

    url = "https://github.com/DanielGarcin/streamlitapp/blob/main/DATA/shopping_behavior_updated.csv?raw=true"
    return pd.read_csv(url)

# Sidebar pour le chargement des données
st.sidebar.title("Source de données")
source_option = st.sidebar.radio(
    "Choisir la source de données:",
    ["Données de comportement d'achats", "Télécharger un fichier CSV"]
)

# Initialiser la connexion DuckDB
conn = duckdb.connect(database=':memory:', read_only=False)

# Obtenir les données
if source_option == "Données de comportement d'achats":
    df = charger_donnees_comportement_achat()
    st.sidebar.success("Données de comportement d'achats chargées!")
    
    # Enregistrer les données dans DuckDB
    conn.execute("CREATE TABLE IF NOT EXISTS comportement_achat AS SELECT * FROM df")
    
else:
    uploaded_file = st.sidebar.file_uploader("Télécharger un fichier CSV", type=["csv"])
    if uploaded_file is not None:
        # Sauvegarder temporairement le fichier
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Créer une table à partir du CSV avec DuckDB
        conn.execute(f"CREATE TABLE IF NOT EXISTS comportement_achat AS SELECT * FROM read_csv_auto('{tmp_path}')")
        
        # Charger les données pour affichage
        df = conn.execute("SELECT * FROM comportement_achat").fetchdf()
        st.sidebar.success(f"{len(df)} achats réalisés!")
        
        # Supprimer le fichier temporaire
        os.unlink(tmp_path)
    else:
        st.info("Veuillez télécharger un fichier CSV ou utiliser les données de démonstration.")
        st.stop()

# Afficher un aperçu des données
st.subheader("Aperçu des données")
st.dataframe(df.head(10))


# Statistiques générales
st.header("Statistiques générales")

# Utiliser DuckDB pour les statistiques générales sur les comprtements d'achat
df_total_buyers = conn.execute('select  count(*) as total_buyers from comportement_achat').fetchdf()
df_total_buyers_male = conn.execute("select count(*) as total_buyers_male from comportement_achat where Gender = 'Male' ").fetchdf()
df_total_buyers_female = conn.execute("select count(*) as total_buyers_female  from comportement_achat where Gender = 'Female' ").fetchdf()

col1, col2, col3 = st.columns(3)
col1.metric("Nombre total d'acheteurs", df_total_buyers['total_buyers'][0])
col2.metric("Nombre total d'acheteurs hommes", df_total_buyers_male['total_buyers_male'][0])
col3.metric("Nombre total d'acheteurs femmes", df_total_buyers_female['total_buyers_female'][0])


# Création graphique
st.header("Analyse des acheteurs en fonction d'unbe soubscrition")

# 1. Graphique du nombre d'acheteurs en fonction d'un abonnement ou non
buyers_by_subscription = conn.execute("""
    SELECT 
        "Subscription Status",
        SUM(CASE WHEN "Subscription Status" = 'Yes' THEN 1 ELSE 0 END) as buyers_with_subscription,
        SUM(CASE WHEN "Subscription Status" = 'No' THEN 1 ELSE 0 END) as buyers_without_subscription,
        COUNT(*) as total
    FROM comportement_achat
    GROUP BY 1
    ORDER BY 1
                                      
                                      
""").fetchdf()

 # Créer un graphique à barres en fonction de subscription ou non
fig = go.Figure()
    
fig.add_trace(go.Bar(
        x=buyers_by_subscription["Subscription Status"],
        y=buyers_by_subscription["buyers_with_subscription"],
        name='With Subscription',
         text=buyers_by_subscription["buyers_with_subscription"],
        marker_color='green'
    ))

fig.add_trace(go.Bar(
        x=buyers_by_subscription["Subscription Status"],
        y=buyers_by_subscription["buyers_without_subscription"],
        name='Witout Subscription',
        text=buyers_by_subscription["buyers_without_subscription"],
        marker_color='red'
    ))

st.plotly_chart(fig, use_container_width=True)




st.header("Analyse des acheteurs en fonction d'un discount")

buyers_with_discount = conn.execute("""
    SELECT 
        "Discount Applied",
        SUM(CASE WHEN "Discount Applied" = 'Yes' THEN 1 ELSE 0 END) as buyers_with_discount,
        SUM(CASE WHEN "Discount Applied" = 'No' THEN 1 ELSE 0 END) as buyers_without_discount,
        COUNT(*) as total
    FROM comportement_achat
    GROUP BY 1
    ORDER BY 1
                                      
                                      
""").fetchdf()


# Créer un graphique à barres en fonction de discount ou non
fig = go.Figure()
    
fig.add_trace(go.Bar(
        x=buyers_with_discount["Discount Applied"],
        y=buyers_with_discount["buyers_with_discount"],
        name='With Discount',
         text=buyers_with_discount["buyers_with_discount"],
        marker_color='green'
    ))

fig.add_trace(go.Bar(
        x=buyers_with_discount["Discount Applied"],
        y=buyers_with_discount["buyers_without_discount"],
        name='Without Discount',
        text=buyers_with_discount["buyers_without_discount"],
        marker_color='red'
    ))

st.plotly_chart(fig, use_container_width=True)