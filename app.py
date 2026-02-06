import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Healthcare vs Life Expectancy", layout="wide")

@st.cache_data
def load_data():
    # IMPORTANT: use relative path for Streamlit Cloud
    df = pd.read_csv("who_life_exp.csv")
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.dropna(subset=["life_expectancy", "current_health_expenditure_gdp"])
    return df

df = load_data()

st.title("Healthcare Expenditure and Life Expectancy Across Nations")

# Sidebar filters
countries = st.multiselect(
    "Select Countries",
    options=sorted(df["country"].unique()),
    default=["United States of America", "Japan", "Germany"]
)

year_range = st.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (2000, 2015)
)

filtered_df = df[
    (df["country"].isin(countries)) &
    (df["year"].between(year_range[0], year_range[1]))
]

# -------------------------------
# Scatter Plot
# -------------------------------
st.subheader("Healthcare Spending vs Life Expectancy")

fig, ax = plt.subplots()

for country in filtered_df["country"].unique():
    country_df = filtered_df[filtered_df["country"] == country]
    ax.scatter(
        country_df["current_health_expenditure_gdp"],
        country_df["life_expectancy"],
        label=country,
        alpha=0.7
    )

ax.set_xlabel("Healthcare Expenditure (% of GDP)")
ax.set_ylabel("Life Expectancy (Years)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# -------------------------------
# Line Plot
# -------------------------------
st.subheader("Life Expectancy Trends Over Time")

fig, ax = plt.subplots()

for country in filtered_df["country"].unique():
    country_df = filtered_df[filtered_df["country"] == country]
    ax.plot(
        country_df["year"],
        country_df["life_expectancy"],
        marker="o",
        label=country
    )

ax.set_xlabel("Year")
ax.set_ylabel("Life Expectancy (Years)")
ax.legend()
ax.grid(True)

st.pyplot(fig)