import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu

# Configurer la page
st.set_page_config(page_title="Gestion des Employés", page_icon="👥", layout="wide")




# Fonction pour récupérer les données de la base de données
def get_data_from_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="effdb"
        )
        query = "SELECT * FROM base111"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Erreur de connexion à la base de données : {err}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

# Fonction pour ajouter un employé dans la base de données
def insert_data_into_database(cin, name, site, function, department, contract_type):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="effdb"
        )
        cursor = conn.cursor()

        # Use backticks for column names with spaces
        insert_query = """
        INSERT INTO base111 (cin, nom_prenom, site, fonction, departement, type_contrat)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (cin, name, site, function, department, contract_type))
        conn.commit()

        cursor.close()
        conn.close()
        st.success("Les données ont été ajoutées avec succès à la base de données.")
    except mysql.connector.Error as err:
        st.error(f"Erreur lors de l'insertion des données : {err}")



# Fonction pour supprimer un employé de la base de données
def delete_data_from_database(cin):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="effdb"
        )
        cursor = conn.cursor()

        delete_query = "DELETE FROM base111 WHERE cin = %s"
        cursor.execute(delete_query, (cin,))
        conn.commit()

        cursor.close()
        conn.close()
        st.success(f"L'employé avec CIN {cin} a été supprimé avec succès.")
    except mysql.connector.Error as err:
        st.error(f"Erreur lors de la suppression des données : {err}")



# Charger les données de la base de données MySQL
df = get_data_from_database()

# Vérifiez que les données ont bien été récupérées avant de continuer
if df.empty:
    st.error("Aucune donnée n'a été récupérée depuis la base de données.")
else:
    st.subheader("🔔 Gestion des Employés")

    # Image dans la barre latérale
    st.sidebar.image("data/medina.png", caption="HR Analytics")

    # Menu de navigation dans la barre latérale
    menu_option = option_menu(
        menu_title="Menu Principal",
        options=["Afficher Employés", "Ajouter Employé", "Supprimer Employé"],
        icons=["list", "person-plus", "person-x"],
        menu_icon="cast",
        default_index=0
    )

    # ------------------- Afficher les employés -------------------
    if menu_option == "Afficher Employés":
        st.subheader("Liste des Employés")
        st.dataframe(df)

    # ------------------- Ajouter un employé -------------------
    elif menu_option == "Ajouter Employé":
        st.subheader("Ajouter un nouvel employé")
        with st.form("add_employee_form"):
            cin = st.text_input("cin")
            name = st.text_input("nom_prenom")
            site = st.text_input("site")
            function = st.text_input("fonction")
            department = st.text_input("departement")
            contract_type = st.text_input("type_contrat")
            submit_button = st.form_submit_button("Ajouter")

            if submit_button:
                if cin and name and site and function and department and contract_type:
                    # Check if CIN already exists in the database
                    if cin in df["cin"].values:
                        st.error(f"Un employé avec le CIN {cin} existe déjà.")
                    else:
                        insert_data_into_database(cin, name, site, function, department, contract_type)
                else:
                    st.error("Tous les champs doivent être remplis pour ajouter un employé.")

    # ------------------- Supprimer un employé -------------------
    elif menu_option == "Supprimer Employé":
        st.subheader("Supprimer un employé")
        # Dropdown to select the CIN of the employee to delete
        if not df.empty:
            cin_to_delete = st.selectbox("Sélectionner le CIN de l'employé à supprimer", df["cin"])
            if st.button("Supprimer"):
                delete_data_from_database(cin_to_delete)
        else:
            st.warning("Aucun employé n'est disponible pour être supprimé.")

    # Masquer le menu Streamlit par défaut
    hide_st_style = """
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
