import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurer la page (doit être le premier appel dans le script)
st.set_page_config(page_title="Dashboard Effectif", page_icon="👥", layout="wide")

# Connexion à la base de données MySQL
def get_data_from_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="effdb"
        )
        query = "SELECT cin, nom_prenom, site, fonction, departement, type_contrat FROM base111"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Erreur de connexion à la base de données : {err}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

# Charger les données de la base de données MySQL
df = get_data_from_database()

# Vérifiez que les données ont bien été récupérées avant de continuer
if df.empty:
    st.error("Aucune donnée n'a été récupérée depuis la base de données.")
else:
    st.subheader("🔔 Dashboard des Effectifs")

    # Image dans la barre latérale
    st.sidebar.image("data/medina.png", caption="HR Analytics")

    # ------------------- Création des filtres -------------------
    st.sidebar.header("Filtres")

    # Filtrer par site
    site = st.sidebar.multiselect(
        "Sélectionner un site",
        options=df["site"].unique(),
        default=df["site"].unique()
    )

    # Filtrer par département avec SelectBox (ajout de l'option "Tous")
    departement = st.sidebar.selectbox(
        "Sélectionner un département",
        options=["Tous"] + list(df["departement"].unique())
    )

    # Filtrer par type de contrat
    type_contrat = st.sidebar.multiselect(
        "Sélectionner un type de contrat",
        options=df["type_contrat"].unique(),
        default=df["type_contrat"].unique()
    )

    # Appliquer les filtres sélectionnés
    df_selection = df[df["site"].isin(site) & df["type_contrat"].isin(type_contrat)]
    
    # Appliquer le filtre par département si un département spécifique est sélectionné
    if departement != "Tous":
        df_selection = df_selection[df_selection["departement"] == departement]

    # Fonction pour afficher les données sous forme de tableau (tabular)
    def Home():
        with st.expander("Tabular"):
            showData = st.multiselect('Filter: ', df_selection.columns, default=[])
            st.write(df_selection[showData])

    # Afficher les statistiques principales
    total_effectif = len(df_selection)
    departement_unique = df_selection['departement'].nunique()
    site_unique = df_selection['site'].nunique()

    # Affichage des indicateurs
    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        st.info('Total des employés', icon="📌")
        st.metric(label="Total des employés", value=f"{total_effectif:,.0f}")

    with col2:
        st.info('Nombre de départements', icon="📌")
        st.metric(label="Nombre de départements", value=f"{departement_unique:,.0f}")

    with col3:
        st.info('Nombre de sites', icon="📌")
        st.metric(label="Nombre de sites", value=f"{site_unique:,.0f}")

    st.markdown("---")

    # Graphiques pour la visualisation
    def display_graphs():
        # Effectif par site
        effectif_par_site = df_selection.groupby('site').size().reset_index(name='Effectif')
        fig_site = px.bar(effectif_par_site, x='Effectif', y='site', title="Effectif par Site", template="plotly_white", orientation="h")

        # Effectif par département
        effectif_par_departement = df_selection.groupby('departement').size().reset_index(name='Effectif')
        fig_departement = px.bar(effectif_par_departement, x='departement', y='Effectif', title="Effectif par Département", template="plotly_white", barmode="relative")

        # Effectif par type de contrat
        effectif_par_type_contrat = df_selection.groupby('type_contrat').size().reset_index(name='Effectif')
        fig_type_contrat = px.pie(effectif_par_type_contrat, values='Effectif', names='type_contrat', title="Répartition par Type de contrat", template="plotly_white")

        # Affichage des graphiques
        st.plotly_chart(fig_site, use_container_width=True)
        st.plotly_chart(fig_departement, use_container_width=True)
        st.plotly_chart(fig_type_contrat, use_container_width=True)

    # Fonction de barre latérale et navigation
    def sideBar():
        with st.sidebar:
            selected = option_menu(
                menu_title="Menu Principal",
                options=["Tableau", "Graphiques"],
                icons=["table", "bar-chart"],
                menu_icon="cast",
                default_index=0,
            )

        if selected == "Tableau":
            st.subheader(f"Page: {selected}")
            Home()

        elif selected == "Graphiques":
            st.subheader(f"Page: {selected}")
            display_graphs()

    # Appeler la fonction de navigation dans la barre latérale
    sideBar()

    # Masquer le menu Streamlit par défaut
    hide_st_style = """
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
