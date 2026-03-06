import streamlit as st
import pandas as pd

# Use full page width
st.set_page_config(layout="wide")

# Header
st.header("Worldwide Analysis of Quality of Life and Economic Factors")

# Subtitle
st.write("""This app enables you to explore the relationships between poverty, 
            life expectancy, and GDP across various countries and years. 
            Use the panels to select options and interact with the data.""")

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"
    return pd.read_csv(url)

df = load_data()

# Create 3 tabs
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])

with tab1:
    st.write("Global Overview content goes here")

with tab2:
    st.write("Country Deep Dive content goes here")

with tab3:
    st.subheader("Data Explorer")
    
    # Multiselect for countries
    countries = st.multiselect(
        "Select countries:",
        options=df["country"].unique(),
        default=df["country"].unique()[:5]  # Default to first 5 countries
    )
    
    # Slider for year range
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    year_range = st.slider(
        "Select year range:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Filter data
    filtered_df = df[
        (df["country"].isin(countries)) &
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]
    
    # Show filtered data
    st.dataframe(filtered_df)
    
    # Download button
    st.download_button(
        label="Download filtered data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )