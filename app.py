import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Healthcare vs Life Expectancy", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("C:\\Users\\SAINADH\\Downloads\\OneDrive\\Documents\\Desktop\\who_life_exp.csv")
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

# Scatter plot
st.subheader("Healthcare Spending vs Life Expectancy")
fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="current_health_expenditure_gdp",
    y="life_expectancy",
    hue="country",
    ax=ax
)
st.pyplot(fig)

# Trend plot
st.subheader("Life Expectancy Trends Over Time")
fig, ax = plt.subplots()
sns.lineplot(
    data=filtered_df,
    x="year",
    y="life_expectancy",
    hue="country",
    ax=ax
)
st.pyplot(fig)