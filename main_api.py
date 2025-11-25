# Streamlit DEMO
# python streamlit C:\Users\Laura\Documents\Python_Scripts\Streamlit_Demo\main_api.py
import streamlit as st
import plotly.express as px
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Gapminder Dashboard", layout="wide")

# Load dataset
df = px.data.gapminder()

# Title
st.title("World Bank GDP x life expectancy Timeseries")

# Optional: Add some statistics
st.subheader("Quick Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Countries", df['country'].nunique())

with col2:
    st.metric("Years Covered", f"{df['year'].min()} - {df['year'].max()}")

with col3:
    st.metric("Average GDP", f"{df['gdpPercap'].mean():.2f}")

with col4:
    st.metric("Average life expectancy", f"{df['lifeExp'].mean():.2f}")
    
# Create the plot
fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year",
                 animation_group="country", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60,
                 range_x=[100, 100000], range_y=[25, 90])

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Optional: Show filtered data
if st.checkbox("Show data"):
    st.dataframe(df)
# Add download button at the top
csv = df.to_csv(index=False)
#
with col4:
    st.download_button(
        label="📥 Download Dataset as CSV",
        data=csv,
        file_name="gapminder_data.csv",
        mime="text/csv"
    )
