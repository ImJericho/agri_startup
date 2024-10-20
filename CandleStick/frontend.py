import streamlit as st
import pandas as pd
import mongo_dao as md
import plotly.express as px
import display
import main

st.title("Commodity Market Prices")

commodity_list = main.find_all_commodities_of_intrest()
mongo_dao = md.mongo_dao()

# Dropdown for selecting commodity
commodity = st.selectbox("Select Commodity", commodity_list)

# State initialization for selected markets
if 'selected_markets' not in st.session_state:
    st.session_state.selected_markets = ["Shajapur", "Agar", "Neemuch"]

# Multiselect for market selection
markets = st.multiselect(
    'Select Markets:',
    options=["Shajapur", "Agar", "Neemuch"],
    default=["Neemuch"]
)


# Button for submission
if st.button("Submit"):
    # Fetch data from Atlas
    data = mongo_dao.find_commodities(commodity=commodity)
    data = display.process_data(data)

    # Filter the data based on the selected markets

    filtered_df = data[data["Market Name"].isin(markets)]
    print(filtered_df)
    st.plotly_chart(display.candlestick_chart(filtered_df))
    st.plotly_chart(display.time_series_graph(filtered_df))
