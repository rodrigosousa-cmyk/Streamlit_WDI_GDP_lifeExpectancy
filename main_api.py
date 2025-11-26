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
    fig.update_layout(height=550, margin=dict(l=0, r=0, t=20, b=0))
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
    fig.update_layout(height=700, margin=dict(l=0, r=0, t=20, b=0))
    return fig# Function Sunburst graph
# Function Sumburst Graph
def fn_sunburst(data,year):
    fig = px.sunburst(data[data['year'] == year],
                    path=['continent', 'gdp_perc','country'],
                    values='gdpPercap',#chunck size
                    color='lifeExp',#chunck color
                    hover_data=['year','gdpPercap'],
                    color_continuous_scale='RdBu',
                    # title=f'Life Expectancy vs GDP PerCapta ({year})'
                     )
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=0, b=0))
    return fig
# end of functions
# Set page config
st.set_page_config(page_title="World Bank GDP x life expectancy Timeseries", layout="wide")

# Inject compact CSS to reduce header, margins and font sizes
st.markdown(
    """
    <style>
    /* Reduce padding of the main block container */
    .block-container {
        padding-top: 0.5rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 0.5rem;
    }

    /* Hide Streamlit's top header to gain space */
    header {visibility: hidden;}

    /* Smaller headings globally */
    h1 {font-size:14px !important; margin: 0.25rem 0 !important; padding: 0 !important;}
    h2 {font-size:16px !important; margin: 0.2rem 0 !important; padding: 0 !important;}
    h3 {font-size:20px !important; margin: 0.15rem 0 !important; padding: 0 !important;}

    /* Reduce spacing for tabs and controls */
    [role="tablist"] {margin-bottom: 0.25rem !important;}
    .stSelectbox, .stSlider, .stRadio {margin-bottom: 0.2rem !important;}

    /* Tighter paragraphs / markdown */
    .css-1d391kg p, .streamlit-expanderHeader {margin: 0.1rem 0 !important;}

    /* Metric font adjustments (fallback) */
    .stMetric > div {font-size:14px !important;}

    /* Fallback container padding selector for newer Streamlit versions */
    [data-testid="stAppViewContainer"] .main .block-container {padding-top: 0.5rem; padding-bottom: 0.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Load dataset
#@st.cache_data()
df = px.data.gapminder()
df['gdp_perc'] = pd.qcut(df['gdpPercap'],4,labels=['GDP_Q1','GDP_Q2','GDP_Q3','GDP_Q4'])
# Add download button at the top
csv = df.to_csv(index=False)

# Optional: Add some statistics
# st.subheader("Quick Statistics")
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.metric("Total Countries", df['country'].nunique())
    
# with col2:
#     st.metric("Years Covered", f"{df['year'].min()} - {df['year'].max()}")

# with col3:
#     st.metric("Average GDP", f"{df['gdpPercap'].mean():.2f}")

# with col4:
#     st.metric("Average life expectancy", f"{df['lifeExp'].mean():.2f}")
    
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
        value=years[-1],
        width=600
    )
    st.plotly_chart(fn_sunburst(df, selected_year), use_container_width=True)
# END #

















