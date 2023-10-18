# Project 4

**Note**: For the final result of this project, please visit [here](https://us-vehicle-market-dashboard.onrender.com/).

## Overview
This project focuses on building a Streamlit web application that serves as a dashboard for the US vehicle market. The data for this dashboard is sourced from the `vehicles_us.csv` file. The web application is hosted on Render, offering users an interactive platform to explore various facets of the vehicle market.

## Tools Used
- `numpy`: Fundamental package for scientific computing in Python.
- `pandas`: Essential library for data manipulation and analysis.
- `plotly`: A graphing library to create interactive visualizations.
- `streamlit`: An open-source app framework tailored for Machine Learning and Data Science projects.
- `render`: A cloud service to deploy web applications.

## Exploratory Data Analysis (EDA)
The project commenced with an exploratory data analysis on the dataset, which can be found in the `EDA.ipynb` notebook. During this phase, we conducted:
- **Categorical Distributions Analysis**: Using pie charts, we visualized the distribution of various categories such as model, condition, fuel, transmission, and type.
- **Price Distribution Analysis**: We examined the distribution of vehicle prices using histograms.
- **Price vs. Odometer Analysis**: A scatter plot was used to visualize the relationship between vehicle prices and their odometer readings.
- **Listing Duration Trend Analysis**: We observed how long vehicles remained listed over time using a line chart.

All these visualizations and analyses set the stage for the Streamlit web application. In the app, these charts are further enhanced with interactive filters, granting users the flexibility to delve deeper into the data for each manufacturer in the US.
