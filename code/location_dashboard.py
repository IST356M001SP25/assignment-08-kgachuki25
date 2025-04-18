'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")

tickets_df = pd.read_csv("cache/tickets_in_top_locations.csv")

# Getting locations for selection box
locations = tickets_df["location"].unique()

# Setting up streamlit
st.title("Top Locations for Parking Tickets")
location = st.selectbox("Select a location: ", options = locations)

if location:
    # Filter df based on location:
    tickets_filtered = tickets_df[tickets_df["location"] == location]
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total tickets issued: ", len(tickets_filtered))
        ## set up pyplot
        plot1, series1 = plt.subplots()
        sns.barplot(data = tickets_filtered, x="dayofweek", y="count", estimator="sum", hue="hourofday", ax=series1).set_title("Tickets by Day of Week")
        st.pyplot(plot1)

    with col2:
        st.metric("Total amount of Fines: ", f"${tickets_filtered['amount'].sum()}")
        plot2, series2 = plt.subplots()
        sns.lineplot(tickets_filtered, x = "hourofday", y = "count", estimator = "sum", ax = series2, errorbar = None).set_title("Tickets by Hour of Day")
        st.pyplot(plot2)

    st.map(tickets_filtered[['lat', 'lon']])