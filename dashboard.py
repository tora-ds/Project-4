import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from datetime import datetime

# Settings
st.set_page_config(
    page_title="U.S. Vehicle Market Dashboard",
    layout="wide"
)

reduce_header_height = """
    <style>
        div.block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
"""
st.markdown(reduce_header_height, unsafe_allow_html=True)

add_column_border = """
    <style type="text/css">
        div[data-testid="stHorizontalBlock"] > div {
            border: 0.5px solid #9598a6;
            padding: 10px;
            margin: -5px;
            border-radius: 10px;
            background: transparent;
        }
    </style>
"""
st.markdown(add_column_border, unsafe_allow_html=True)

remove_expander_border = """
    <style>
        ul.streamlit-expander {
            border: 0px solid #9598a6 !important;
    </style>
"""
st.markdown(remove_expander_border, unsafe_allow_html=True)

st.write("<style>div.row-widget.stRadio > div{flex-direction: row; justify-content: center;}</style>", unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align: center; margin-bottom: 20px;'>U.S. Vehicle Market Dashboard</h1>", unsafe_allow_html=True)

# Data loading
@st.cache_data
def fetch_and_clean_data():
    df = pd.read_csv("vehicles_us.csv")
    df = df.dropna(subset=["model_year"]).reset_index(drop=True)
    df["date_posted"] = pd.to_datetime(df["date_posted"])
    df["manufacturer"] = df["model"].apply(lambda x: x.split()[0])
    df["model_year"] = df["model_year"].astype(int)
    return df

df = fetch_and_clean_data()

# Filters
st.markdown("<h3>🔍 Filters</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Date range filter
filter_date_range = col1.date_input(
    label="Select Date Range",
    value=(df["date_posted"].min(), df["date_posted"].max())
)

# Manufacturer filter
df_date_filtered = df[
    (df["date_posted"] >= datetime.combine(filter_date_range[0], datetime.min.time())) &
    (df["date_posted"] <= datetime.combine(filter_date_range[1], datetime.max.time()))
]
manufacturers = np.sort(df_date_filtered["manufacturer"].unique())
default_index = int(np.where(manufacturers == "ford")[0][0]) if "ford" in manufacturers else 0

filter_manufacturer = col2.selectbox(
    label="Select Manufacturer",
    options=manufacturers,
    index=default_index
)

# Model year filter
filter_model_year = col3.selectbox(
    label="Select Model Year",
    options=np.sort(df_date_filtered[df_date_filtered["manufacturer"] == filter_manufacturer]["model_year"].unique())[::-1],
    index=0
)

# Slicing the data
df = df[
    (df["date_posted"] >= datetime.combine(filter_date_range[0], datetime.min.time())) &
    (df["date_posted"] <= datetime.combine(filter_date_range[1], datetime.max.time())) &
    (df["manufacturer"] == filter_manufacturer) &
    (df["model_year"] == filter_model_year)
]

# Charts
st.markdown("<h3>📊 Charts</h3>", unsafe_allow_html=True)

# Data overview
col1 = st.columns(1)[0]
with col1.expander("Click here to view the data overview"):
    st.dataframe(df, use_container_width=True)

# Pie charts
def create_pie_chart(df, column_name):
    fig = px.pie(df, names=column_name, hole=0.4)
    fig.update_traces(
        textposition="inside",
        hoverinfo="label+percent+value",
        hovertemplate="%{label}<br>%{value}"
    )
    fig.update_layout(
        showlegend=False,
        height=220,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    return fig

columns_for_pie = ["model", "condition", "fuel", "transmission", "type"]

st_cols = st.columns(5)
for i, col_name in enumerate(columns_for_pie):
    st_cols[i].markdown(f"<h5>{col_name.capitalize()}</h5>", unsafe_allow_html=True)
    st_cols[i].plotly_chart(create_pie_chart(df, col_name), use_container_width=True)

# Histogram & scater plot
col1, col2 = st.columns(2)

# Price distribution
with col1:
    st.markdown("<h5>Distribution of Prices</h5>", unsafe_allow_html=True)

    normalize = st.checkbox("Normalize Histogram")
    histnorm_value = "percent" if normalize else None

    choose = st.radio(
        label="label",
        options=["none", "model", "condition", "fuel", "transmission", "type"],
        label_visibility="collapsed"
    )

    if choose == "none":
        fig = px.histogram(df, x="price", histnorm=histnorm_value)
    else:
        fig = px.histogram(df, x="price", color=choose, histnorm=histnorm_value)

    fig.update_layout(
        xaxis_title=None,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        height=300,
        margin=dict(t=0, b=0, l=0, r=0),
        legend_orientation="h",
        legend=dict(y=-0.2, x=0.5, xanchor="center", title_text="") if choose != "none" else None
    )

    st.plotly_chart(fig, use_container_width=True)

# Price vs. odometer
with col2:
    st.markdown("<h5>Price vs. Odometer</h5>", unsafe_allow_html=True)
    
    regression_line = st.checkbox("Add Regression Line")
    trendline_arg = "ols" if regression_line else None
    
    fig = px.scatter(df, x="odometer", y="price", trendline=trendline_arg)
    fig.update_layout(
        xaxis_title="Odometer",
        yaxis_title="Price",
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        height=340,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    fig.update_traces(marker=dict(size=10))

    st.plotly_chart(fig, use_container_width=True)

# Days listed
col1 = st.columns(1)[0]
col1.markdown("<h5>Total Days Vehicles Were Listed Each Day</h5>", unsafe_allow_html=True)

df_trend = df.set_index("date_posted").resample("D").sum()

fig = px.line(df_trend, x=df_trend.index, y="days_listed")
fig.update_layout(
    xaxis_title=None,
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    height=300,
    margin=dict(t=0, b=0, l=0, r=0),
)

col1.plotly_chart(fig, use_container_width=True)
