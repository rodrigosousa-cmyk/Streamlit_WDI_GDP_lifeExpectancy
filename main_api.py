# deploy API at: https://share.streamlit.io/deploy
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
# Scatterplot Timeseries Function
def fn_scatterplot(df):
        fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year",
                         animation_group="country", size="pop", color="continent",
                         hover_name="country", log_x=True, size_max=60,
                         range_x=[100, 100000], range_y=[25, 90])
        return fig
# Function Create choropleth map
def create_choropleth(df,indicator):
    # Use percentiles to exclude outliers
    valid_data = df[indicator].dropna()
    
    if len(valid_data) > 0:
        # Get 5th and 95th percentiles to exclude extremes
        p5 = np.percentile(valid_data, 10)
        p95 = np.percentile(valid_data, 90)
        
        # Apply log scaling with buffer
        min_val = max(p5 * 0.1, valid_data.min())  # Don't go below actual min
        max_val = min(p95 * 10, valid_data.max())  # Don't go above actual max
    else:
        min_val, max_val = 1e3, 1e9
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color=indicator,
        hover_name="country",
        animation_frame="year",
        #title=str('CO2 '+indicator),
        color_continuous_scale='Plasma',
        #range_color=[1e3, 1e10] # Changed from range_x to range_color
        range_color=[min_val, max_val]
    )
    fig.update_layout(height=600, margin=dict(l=0, r=0, t=50, b=0))
    return fig
# end of function
# Set page config
st.set_page_config(page_title="World Bank GDP x life expectancy Timeseries", layout="wide")
# Title
# Load dataset
#@st.cache_data()
df = px.data.gapminder()
# Add download button at the top
csv = df.to_csv(index=False)

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
    
# Display plots in tabs
tab1, tab2 ,tab3 = st.tabs(["🌍 Annual GDP per capita", "🌍 Life Expectancy by year", "📊 GDP x Life Expectancy TimeSeries"]) 

with tab1:
    st.plotly_chart(create_choropleth(df,"gdpPercap"), use_container_width=True)
    
with tab2:
    st.plotly_chart(create_choropleth(df,"lifeExp"), use_container_width=True)
    
with tab3:
    # Display the plot
    st.plotly_chart(fn_scatterplot(df), use_container_width=True)
    # Optional: Show filtered data
    if st.checkbox("Show data"):
        st.dataframe(df)
    #
    st.download_button(
        label="📥 Download Dataset as CSV",
        data=csv,
        file_name="wdi_gapminder_data.csv",
        mime="text/csv"
    )






