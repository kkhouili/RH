import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu

# Configurer la page
st.set_page_config(page_title="Gestion des Sites", page_icon="👥", layout="wide")




# Fonction pour récupérer les données de la base de données
def get_data_from_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mydb"
        )
        query = "SELECT * FROM testfp"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Erreur de connexion à la base de données : {err}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

# Fonction pour ajouter un employé dans la base de données
def insert_data_into_database(site, rb, frais_personnel, chiffre_affaire, fp_ca, date):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mydb"
        )
        cursor = conn.cursor()
        
        

        # Use backticks for column names with spaces
        insert_query = """
        INSERT INTO testfp (site, rb, frais_personnel, chiffre_affaire, fp_ca, date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (site, rb, frais_personnel, chiffre_affaire, fp_ca, date))
        conn.commit()

        cursor.close()
        conn.close()
        st.success("Les données ont été ajoutées avec succès à la base de données.")
    except mysql.connector.Error as err:
        st.error(f"Erreur lors de l'insertion des données : {err}")



# Fonction pour supprimer un employé de la base de données
def delete_data_from_database(site):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mydb"
        )
        cursor = conn.cursor()

        delete_query = "DELETE FROM testfp WHERE site = %s"
        cursor.execute(delete_query, (site,))
        conn.commit()

        cursor.close()
        conn.close()
        st.success(f"Le site avec le nom {site} a été supprimé avec succès.")
    except mysql.connector.Error as err:
        st.error(f"Erreur lors de la suppression des données : {err}")



# Charger les données de la base de données MySQL
df = get_data_from_database()

# Vérifiez que les données ont bien été récupérées avant de continuer
if df.empty:
    st.error("Aucune donnée n'a été récupérée depuis la base de données.")
else:
    st.subheader("🔔 Gestion des Site")

    # Image dans la barre latérale
    st.sidebar.image("data/medina.png", caption="HR Analytics")

    # Menu de navigation dans la barre latérale
    menu_option = option_menu(
        menu_title="Menu Principal",
        options=["Afficher Site", "Ajouter site", "Supprimer Site"],
        icons=["list", "person-plus", "person-x"],
        menu_icon="cast",
        default_index=0
    )

    # ------------------- Afficher les employés -------------------
    if menu_option == "Afficher Site":
        st.subheader("Liste des Site")
        st.dataframe(df)

    # ------------------- Ajouter un employé -------------------
    elif menu_option == "Ajouter site":
        st.subheader("Ajouter un nouvel employé")
        with st.form("add_employee_form"):
            site = st.text_input("site")
            rb = st.text_input("rb")
            frais_personnel = st.text_input("frais_personnel")
            chiffre_affaire = st.text_input("chiffre_affaire")
            fp_ca = st.text_input("fp_ca")
            date = st.text_input("date")
            submit_button = st.form_submit_button("Ajouter")

            if submit_button:
                if site and rb and frais_personnel and chiffre_affaire and fp_ca and date:
                    # Check if site already exists in the database
                    if site in df["site"]:
                        st.error(f"Un site avec le nom {site} existe déjà.")
                    else:
                        insert_data_into_database(site, rb, frais_personnel, chiffre_affaire, fp_ca, date)
                else:
                    st.error("Tous les champs doivent être remplis pour ajouter un employé.")

    # ------------------- Supprimer un employé -------------------
    elif menu_option == "Supprimer Site":
        st.subheader("Supprimer un Site")
        # Dropdown to select the CIN of the employee to delete
        if not df.empty:
            site_to_delete = st.selectbox("Sélectionner le nom de Site à supprimer", df["site"])
            if st.button("Supprimer"):
                delete_data_from_database(site_to_delete)
        else:
            st.warning("Aucun Site n'est disponible pour être supprimé.")

    # Masquer le menu Streamlit par défaut
    hide_st_style = """
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
