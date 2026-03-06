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
    st.subheader("Global Overview")
    
    # Year slider
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    selected_year = st.slider(
        "Select year:",
        min_value=min_year,
        max_value=max_year,
        value=max_year,
        key="tab1_year"
    )
    
    # Filter data by selected year
    year_df = df[df["year"] == selected_year]
    
    # Create 4 columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_life_exp = year_df["Life Expectancy (IHME)"].mean()
        st.metric(
            label="Mean Life Expectancy",
            value=f"{avg_life_exp:.1f} years"
        )
    
    with col2:
        median_gdp = year_df["GDP per capita"].median()
        st.metric(
            label="Median GDP per Capita",
            value=f"${median_gdp:,.0f}"
        )
    
    with col3:
        avg_poverty = year_df["headcount_ratio_upper_mid_income_povline"].mean()
        st.metric(
            label="Mean Poverty Rate",
            value=f"{avg_poverty:.1f}%"
        )
    
    with col4:
        num_countries = year_df["country"].nunique()
        st.metric(
            label="Number of Countries",
            value=num_countries
        )



 

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


import plotly.express as px

fig = px.scatter(
    data_frame=df,
    x="GDP per capita",
    y="Life Expectancy (IHME)",
    hover_name="country",
    log_x=True,
    size="Population",
    color = "headcount_ratio_upper_mid_income_povline",
    title="Life Expectancy vs GDP per Capita",
    labels={
    "GDP per capita": "GDP per Capita (USD)",
    "Life Expectancy (IHME)": "Life Expectancy (Years)",
    "headcount_ratio_upper_mid_income_povline": "Poverty Rate (%)",
    "Population": "Population"
}
)

st.plotly_chart(fig, use_container_width=True)


import joblib

@st.cache_resource
def load_model():
    return joblib.load("model.joblib")

model = load_model()

# --- Prediction Section ---
st.subheader("Predict Life Expectancy")

col1, col2, col3, col4 = st.columns(4)

with col1:
    gdp_input = st.number_input(
        "GDP per capita",
        key="gdp_input"
    )

with col2:
    poverty_input = st.number_input(
        "Poverty Rate (%)",
        key="poverty_input"
    )

with col3:
    year_input = st.number_input(
        "Year",
        key="year_input"
    )


input_df = pd.DataFrame({
    "GDP per capita": [gdp_input],
    "headcount_ratio_upper_mid_income_povline": [poverty_input],
    "year": [year_input]
})

prediction = model.predict(input_df)
#st.write(prediction)

with col4:
    st.metric("Predicted Life Expectancy", f"{prediction[0]:.1f} years")