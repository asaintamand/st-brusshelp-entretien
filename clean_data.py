# - note sur le nombre de cas covid en 2020 (ethos 2), inclus dans "hébergement d'urgence"
# - note sur l'absence de catégorie "X" avant 2022
# - pourquoi pénal = 0 tout le temps ?

# %% Packages
import numpy as np
import pandas as pd

# %% Parameters
years = [2008, 2010, 2014, 2016, 2017, 2018, 2020, 2022, 2024]
years_str = [str(year) for year in years]
categories = {
    "Femmes": 3,
    "Hommes": 4,
    "X": 5,
    "Indéterminé": 6,
    "Mineurs": 7,
    "Total": 8,
}
ethos_no = np.arange(1, 8)
ethos_classes_full = [
    "ETHOS Light 1 - Espace public",
    "ETHOS Light 2 - Hébergement d'urgence",
    "ETHOS Light 2 - Plateforme citoyenne",
    # "ETHOS Light 2 - Dispositifs de crise (COVID-19)",
    "ETHOS Light 3 - Maisons d'accueil",
    "ETHOS Light 3 - Logements de transit",
    "ETHOS Light 3 - Dispositifs sociaux en hôtel",
    "ETHOS Light 4 - Institutions médicales",
    "ETHOS Light 4 - Asile",
    # "ETHOS Light 4 - Institutions pénales",
    "ETHOS Light 5 - SHNA",
    "ETHOS Light 5 - Occupations négociées",
    "ETHOS Light 5 - Squats",
    "ETHOS Light 6 - Chez des tiers",
    "ETHOS Light 7 - Sous menace d'expulsion",
]
# ethos_classes_no = [elt[12] for elt in ethos_classes_full]
# ethos_classes_name = [elt[16:] for elt in ethos_classes_full]
ethos_classes_ligne = [5, 6, 7, 9, 10, 11, 17, 18, 13, 14, 15, 20, 21]
ethos_classes_name = [
    "Espace public",
    "Dispositifs d'urgence",
    "Foyer d'hébergement",
    "En institution",
    "Logement non-conventionnel",
    "Chez des tiers",
    "Sous menace d'expulsion",
]
ethos_classes_correspondance = {
    name: no for name, no in zip(ethos_classes_full, ethos_classes_ligne)
}

# %% Data
dfs_source = pd.read_excel("data/Comparatif 2008 - 2024.xlsx", sheet_name=years_str)

# %%
df_clean = pd.DataFrame(
    columns=["year", "EL_no", "EL_name_general", "EL_name_sub", "public", "value"]
)

for year in years:
    df_source = dfs_source[str(year)]
    for cat, cat_corresp in categories.items():
        for el, el_corresp in ethos_classes_correspondance.items():
            el_no = el[12]
            el_name_sub = el[16:]
            el_name_general = f"{el_no} : {ethos_classes_name[int(el_no) - 1]}"
            df_clean.loc[len(df_clean)] = [
                year,
                el_no,
                el_name_general,
                el_name_sub,
                cat,
                df_source.iloc[el_corresp, cat_corresp],
            ]

df_clean["value"] = df_clean["value"].astype("Int64")
df_clean

# %%
df_clean.to_csv("data/clean_data.csv", index=False)
# %%
