import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard TogoShop 🇹🇬")

@st.cache_data
def charger_donnees():
    df = pd.read_csv("ecommerce_togo.csv")

    # Suppression des doublons
    df = df.drop_duplicates()

    # Imputation par la médiane (variables numériques sensibles aux valeurs extrêmes)
    df['age_client'] = df['age_client'].fillna(df['age_client'].median())
    df['anciennete_client_jours'] = df['anciennete_client_jours'].fillna(df['anciennete_client_jours'].median())
    df['delai_livraison_jours'] = df['delai_livraison_jours'].fillna(df['delai_livraison_jours'].median())

    # Une remise manquante = probablement aucune remise appliquée
    df['remise_pct'] = df['remise_pct'].fillna(0)

    return df

df = charger_donnees()

st.write(f"Le dataset contient **{df.shape[0]} commandes** et **{df.shape[1]} colonnes**.")
st.write("Valeurs manquantes restantes :", df.isna().sum().sum())



st.sidebar.header("Filtres")

villes = st.sidebar.multiselect(
    "Ville",
    options=df['ville'].unique(),
    default=df['ville'].unique()
)

categories = st.sidebar.multiselect(
    "Catégorie",
    options=df['categorie'].unique(),
    default=df['categorie'].unique()
)

canal_achat = st.sidebar.multiselect(
    "Canal d'achat",
    options=df['canal_achat'].unique(),
    default=df['canal_achat'].unique()
)

mode_paiement = st.sidebar.multiselect(
    "Mode de paiement",
    options=df['mode_paiement'].unique(),
    default=df['mode_paiement'].unique()
)

df_filtre = df[
    (df['ville'].isin(villes)) &
    (df['categorie'].isin(categories)) &
    (df['canal_achat'].isin(canal_achat)) &
    (df['mode_paiement'].isin(mode_paiement))
]

st.write(f"**{df_filtre.shape[0]} commandes** correspondent à tes filtres.")
st.dataframe(df_filtre.head(10))

st.subheader("Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Chiffre d'affaires", f"{df_filtre['montant_total_fcfa'].sum():,.0f} FCFA")
    
with col2:
    st.metric("Nombre de commandes", f"{df_filtre.shape[0]:,}")
    
with col3:
    st.metric("Panier moyen", f"{df_filtre['montant_total_fcfa'].mean():,.0f} FCFA")
    
with col4:
    st.metric("Satisfaction moyenne", f"{df_filtre['satisfaction_1_5'].mean():.2f} / 5")
    
    

st.subheader("Evolution des ventes dans le temps")

df_mois = df_filtre.groupby('mois').agg({'montant_total_fcfa': 'sum'}).reset_index()

fig_mois = px.line(df_mois, x='mois', y='montant_total_fcfa', title="Chiffre d'affaires par mois")
st.plotly_chart(fig_mois, use_container_width=True)
    
r_ville = df_filtre.groupby('ville').agg(
    nb_commandes=('id_commande', 'count'),
    chiffre_affaires=('montant_total_fcfa', 'sum')
).sort_values(by='nb_commandes', ascending=False).reset_index()

fig_ville = px.bar(
    r_ville, x='ville', y='chiffre_affaires', color='chiffre_affaires',
    title="Chiffre d'affaires par ville"
)
st.plotly_chart(fig_ville, use_container_width=True)

  
  
st.subheader("Heatmap de corrélation")
    
fig, ax = plt.subplots(figsize=(8, 6))
correlation = df_filtre.corr(numeric_only=True)
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
ax.set_title("Heatmap de corrélation")

st.pyplot(fig)



st.subheader("Distribution des montants par catégorie")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x='categorie', y='montant_total_fcfa', data=df_filtre, ax=ax)
ax.set_title("Boxplot du montant total par catégorie")
ax.set_xlabel("Catégorie")
ax.set_ylabel("Montant total (FCFA)")

st.pyplot(fig)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    