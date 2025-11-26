# deploy API at: https://share.streamlit.io/deploy
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
# Scatterplot Timeseries Function
def fn_scatterplot(df):
    fig = px.scatter(
        df,
        x="gdpPercap",
        y="lifeExp",
        animation_frame="year",
        animation_group="iso_alpha",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        log_y=False,
        size_max=50,
        range_x=[df.gdpPercap.min(), df.gdpPercap.max()],
        range_y=[df.lifeExp.min(),df.lifeExp.max()+10],
        # title='Emissions vs Cumulative Emissions Over Time'
    )
    return fig
# Function Create choropleth map
def create_choropleth(df,indicator):
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color=indicator,
        hover_name="country",
        hover_data="gdpPercap",
        animation_frame="year",
        color_continuous_scale='Plasma',
    )
    fig.update_layout(height=600, margin=dict(l=0, r=0, t=50, b=0))
    return fig# Function Sunburst graph
# Function Sumburst Graph
def fn_sunburst(data,year):
    fig = px.sunburst(data[data['year'] == year],
                    path=['continent', 'gdp_perc','country'],
                    values='gdpPercap',#chunck size
                    color='lifeExp',#chunck color
                    hover_data=['year','gdpPercap'],
                    color_continuous_scale='RdBu',
                    title=f'Life Expectancy vs GDP PerCapta ({year})')
    fig.update_layout(height=600, margin=dict(l=0, r=0, t=50, b=0))
    return fig
# end of functions
# Set page config
st.set_page_config(page_title="World Bank GDP x life expectancy Timeseries", layout="wide")
# Load dataset
#@st.cache_data()
df = px.data.gapminder()
df['gdp_perc'] = pd.qcut(df['gdpPercap'],4,labels=['GDP_Q1','GDP_Q2','GDP_Q3','GDP_Q4'])
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
tab1,tab2,tab3,tab4= st.tabs(["🌍 Life Expectancy by year","🌍 Annual GDP per capita",
    "📊 GDP x Life Expectancy TimeSeries","📊 GDP x Life Expectancy (quinquennium)"]) 

with tab1:
    st.plotly_chart(create_choropleth(df,"lifeExp"), use_container_width=True)
        
with tab2:
    st.plotly_chart(create_choropleth(df,"gdp_perc"), use_container_width=True)
    
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
with tab4:
    # Place a slider on top of the sunburst (snaps to available years)
    years = sorted(df['year'].unique().tolist())
    selected_year = st.select_slider(
        "Select year",
        options=years,
        value=years[-1]
    )
    st.plotly_chart(fn_sunburst(df, selected_year), use_container_width=True)
# END #
