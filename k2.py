import streamlit as st
import pandas as pd
import numpy as np  
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import * 
import time

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.subheader("🔔 HR Analytics")
st.markdown("##")

# Assuming 'view_all_data()' fetches your data
result = view_all_data()
df = pd.DataFrame(result, columns=["site", "rb", "frais_personnel", "chiffre_affaire", "fp_ca", "date"])
st.sidebar.image("data/medina.png", caption="Online Analyse")

#-------------------creation filtres-----------------
st.sidebar.header("Filter")
site = st.sidebar.multiselect(
    "Select site",
    options=df["site"].unique(),
    default=df["site"].unique(),
)

Date = st.sidebar.multiselect(
    "Select date",
    options=df["date"].unique(),
    default=df["date"].unique(),
)

# Checkboxes for RB selection
selected_rb = []
for option in df["rb"].unique():
    # Set default to check the checkbox if the option is 24
    is_checked = (option == 24)  # Check if the option is 24 for default selection
    if st.sidebar.checkbox(f"Année courante={option}" if option == 24 else f"Budget={option}" if option == 2024 else f"Année Précédente={option}", value=is_checked):
        selected_rb.append(option)

df_selection = df.query("site == @site & date == @Date & rb in @selected_rb")

# Function for displaying comparison visualization
def comparison_graphs():
    # Calculate totals for the comparison
    totals = {
        "Current Year": df_selection[df_selection["rb"] == 24].sum(),
        "Previous Year": df_selection[df_selection["rb"] == 2023].sum(),
        "Budget": df_selection[df_selection["rb"] == 2024].sum()
    }
    
    # Prepare DataFrame for Plotly
    comparison_df = pd.DataFrame({
        "Year": ["Current Year", "Previous Year", "Budget"],
        "Chiffre Affaire": [totals["Current Year"]["chiffre_affaire"], totals["Previous Year"]["chiffre_affaire"], totals["Budget"]["chiffre_affaire"]],
        "Frais Personnel": [totals["Current Year"]["frais_personnel"], totals["Previous Year"]["frais_personnel"], totals["Budget"]["frais_personnel"]],
    })

    # Create grouped bar chart
    fig_comparison = px.bar(
        comparison_df,
        x="Year",
        y=["Chiffre Affaire", "Frais Personnel"],
        title="<b>Comparison of Current Year, Previous Year, and Budget</b>",
        barmode='group',
        template="plotly_white",
        labels={"value": "Amount (MDT)", "variable": "Category"}
    )
    
    fig_comparison.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False),
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

# Home function for displaying tabular data
def Home():
    with st.expander("Tabular"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=[])
        st.write(df_selection[showData])

# Compute top analytics
total_chiffre_affaire = df_selection["chiffre_affaire"].sum()
chiffre_affaire_mean = df_selection["chiffre_affaire"].mean()

total_Frais_Personnel = df_selection["frais_personnel"].sum()
Frais_Personnel_mean = df_selection["frais_personnel"].mean()

# Display metrics
total1, total2,total4, total5 = st.columns(4, gap='large')

with total1:
    st.info('Total Chiffre Affaire', icon="📌")
    st.metric(label="Sum MDT", value=f"{total_chiffre_affaire:,.0f}")

with total2:
    st.info('Chiffre Affaire Moyen', icon="📌")
    st.metric(label="Mean MDT", value=f"{chiffre_affaire_mean:,.0f}")

with total4:
    st.info('Total Frais du Personnel ', icon="📌")
    st.metric(label="Sum MDT", value=f"{total_Frais_Personnel:,.0f}")

with total5:
    st.info('Frais du Personnel Moyen', icon="📌")
    st.metric(label="Mean MDT", value=f"{Frais_Personnel_mean:,.0f}")

st.markdown("""---""")

# Graphs function for visualizations
def graphs():
    # Group by site and date for Chiffre d'affaire and Frais du personnel
    chiffre_affaire_by_site = df_selection.groupby(by=["site"]).sum()[["chiffre_affaire"]].sort_values(by="chiffre_affaire")
    chiffre_affaire_by_Date = df_selection.groupby(by=["date"]).sum()[["chiffre_affaire"]]
    frais_personnel_by_site = df_selection.groupby(by=["site"]).sum()[["frais_personnel"]].sort_values(by="frais_personnel")
    frais_personnel_by_Date = df_selection.groupby(by=["date"]).sum()[["frais_personnel"]]

    # Chiffre d'affaire by site
    fig_chiffre_affaire = px.bar(
        chiffre_affaire_by_site,
        x="chiffre_affaire",
        y=chiffre_affaire_by_site.index,
        orientation="h",
        title="<b> Chiffre d'affaire par site</b>",
        color_discrete_sequence=["#0083b8"] * len(chiffre_affaire_by_site),
        template="plotly_white",
    )

    fig_chiffre_affaire.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
    )

    # Chiffre d'affaire by date
    fig_chiffre_affaire_Date = px.line(
        chiffre_affaire_by_Date,
        x=chiffre_affaire_by_Date.index,
        y="chiffre_affaire",
        title="<b> Chiffre d'affaire par Date </b>",
        color_discrete_sequence=["#0083b8"] * len(chiffre_affaire_by_Date),
        template="plotly_white",
    )

    fig_chiffre_affaire_Date.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False),
    )

    # Frais du Personnel by site
    fig_frais_personnel = px.bar(
        frais_personnel_by_site,
        x="frais_personnel",
        y=frais_personnel_by_site.index,
        orientation="h",
        title="<b> Frais du Personnel par site</b>",
        color_discrete_sequence=["#0083b8"] * len(frais_personnel_by_site),
        template="plotly_white",
    )

    fig_frais_personnel.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
    )

    # Frais du Personnel by date
    fig_frais_personnel_Date = px.line(
        frais_personnel_by_Date,
        x=frais_personnel_by_Date.index,
        y="frais_personnel",
        title="<b> Frais du Personnel par Date  </b>",
        color_discrete_sequence=["#0083b8"] * len(frais_personnel_by_Date),
        template="plotly_white",
    )

    fig_frais_personnel_Date.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False),
    )

    left, right = st.columns(2)
    left.plotly_chart(fig_chiffre_affaire, use_container_width=True)
    right.plotly_chart(fig_chiffre_affaire_Date, use_container_width=True)

    left, right = st.columns(2)
    left.plotly_chart(fig_frais_personnel, use_container_width=True)
    right.plotly_chart(fig_frais_personnel_Date, use_container_width=True)

def ProgressBar():
    st.markdown("""<style>.stProgress> div > div > div > div > {background-image:linear-gradient(to right, #99ff99 , #FFF00)}</style>""", unsafe_allow_html=True)
    target = 70000  # Set your target value here
    current = df_selection["chiffre_affaire"].sum()

    # Check to avoid division by zero
    if target > 0:
        percent = min(100, max(0, round((current / target) * 100)))  # Ensure the value is between 0 and 100
    else:
        percent = 0  # If the target is 0, set percent to 0

    bar = st.progress(percent)  # Set the progress bar
    time.sleep(1)
    st.markdown(f"### Progress: {percent}%")

# Sidebar options
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # required
        options=["Home", "Graphs", "Comparison", "Progress Bar"],  # required
        icons=["house", "bar-chart", "clipboard-data", "progress-bar"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
    )

if selected == "Home":
    Home()
elif selected == "Graphs":
    graphs()
elif selected == "Comparison":
    comparison_graphs()
elif selected == "Progress Bar":
    ProgressBar()
