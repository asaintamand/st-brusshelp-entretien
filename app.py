# %% Packages
import streamlit as st
import pandas as pd
import plotly.express as px

# import numpy as np

# %% Load data
df = pd.read_csv("data/clean_data.csv")

# Set values as int
df["value"] = df["value"].astype("Int64")

# Remove lines with public "Total"
df_total = df[df["public"] == "Total"]
df_wo_total = df[df["public"] != "Total"]

# %% Layout
st.set_page_config(
    page_title="Données de recensement du sans-abrisme à Bruxelles", layout="wide"
)

st.title(
    "Tableau de bord interactif des données de recensement du sans-abrisme à Bruxelles"
)

# %% Temporal series plot
st.header("Évolution du nombre de personnes par statut")

df_by_EL = df.groupby(["year", "public", "EL_name_general"]).sum().reset_index()
df_by_EL.drop("EL_no", axis=1, inplace=True)

# Filter : public selection
public = df["public"].unique()
public_selection = st.selectbox(
    "Choisir le public à inclure :", public, index=len(public) - 1
)

txt_md = """
Les différents publics représentent les adultes selon leur genre (femmes, hommes, X, genre indéterminé lors des recensements) et les mineurs (sans distinction de genre).

Notes :  
- Avant 2022, le genre 'X' n'était pas repris lors des dénombrements.
- En 2020, les personnes hébergées dans des dispositifs de crise liés à la pandémie de COVID-19 sont incluses dans la catégorie 'Dispositifs d'urgence'.
"""
st.markdown(txt_md)


# Filtering data
df_filtered = df_by_EL[df_by_EL["public"] == public_selection]

# Graphique area
fig_area = px.area(
    df_filtered,
    x="year",
    y="value",
    color="EL_name_general",
    line_group="EL_name_general",
    title=f"Évolution par année et catégorie ETHOS Light ({public_selection})",
    markers=True,
)

fig_area.update_layout(
    xaxis_title="Année",
    yaxis_title="Nombre de personnes",
    hovermode="x unified",
    legend_title_text="Catégorie ETHOS Light",
    margin=dict(l=20, r=20, t=50, b=20),
)

st.plotly_chart(fig_area, use_container_width=True)

st.divider()

# %% Distribution plots by either ETHOS or public
st.header("Répartition par classe ETHOS Light ou par public pour une année donnée")

# Droplist to select year
years_v1 = sorted(df["year"].unique())
year_selection_v1 = st.selectbox(
    "Sélectionner une année :", years_v1, index=len(years_v1) - 1
)

df_year_total = df_total[df_total["year"] == year_selection_v1]
df_year_total.dropna(inplace=True)
df_year_total = df_year_total.sort_values("EL_name_general")

df_year_wo_total = df_wo_total[df_wo_total["year"] == year_selection_v1]
df_year_wo_total = df_year_wo_total.groupby("public", as_index=False).sum()

col1, col2 = st.columns(2)

# --- Plot 1 : distribution by ETHOS ---
with col1:
    st.write(df_year_total.dropna())
    st.subheader("Par catégorie ETHOS Light (tout public confondu)")
    fig_sun_statut = px.pie(
        df_year_total.dropna(),
        values="value",
        names="EL_name_general",
        # hover_name="EL_name_sub",
        # hover_data="value",
        color="EL_name_general",
        # color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(fig_sun_statut, use_container_width=True)

# --- Plot 2 : distribution by public ---
with col2:
    st.subheader("Par genre et âge (toute catégorie ETHOS Light confondue)")
    fig_sun_genre = px.pie(
        df_year_wo_total.dropna(subset=["value", "public"]),
        values="value",
        color="public",
        names="public",
        hover_data="value",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )

    st.plotly_chart(fig_sun_genre, use_container_width=True)

st.divider()

# %% Distribution plots by ETHOS and public
st.header("Répartition par public pour une catégorie ETHOS Light et une année donnés")

years_v2 = sorted(df["year"].unique())

ethos_classes_name = sorted(df["EL_name_general"].unique())

col3, col4 = st.columns(2)

with col3:
    ethos_selection = st.selectbox(
        "Sélectionner une catégorie ETHOS Light :", ethos_classes_name, index=0
    )
with col4:
    year_selection_v2 = st.selectbox(
        "Choisir une année :", years_v2, index=len(years_v2) - 1
    )

df_ethos_year = (
    df_wo_total[df_wo_total["year"] == year_selection_v2][
        df_wo_total["EL_name_general"] == ethos_classes_name[2]
    ]
    .groupby("public")
    .sum()
    .reset_index()
    .drop(["year", "EL_no"], axis=1)
)


# Plot combined
fig_sun_combine = px.pie(
    df_ethos_year.dropna(),
    values="value",
    color="public",
    names="public",
    hover_data="value",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    title=f"Répartition par public pour la catégorie ETHOS Light {ethos_selection} en {year_selection_v2}",
)

fig_sun_combine.update_layout(margin=dict(l=0, r=0, t=50, b=0))

# Center plot
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.plotly_chart(fig_sun_combine, use_container_width=True)
