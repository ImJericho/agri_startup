import streamlit as st
import pandas as pd
import mongo_dao as md
import plotly.express as px
import graph_display as graph_display
import utils

st.title("Crop Market Prices")


mongo_dao = md.mongo_dao()



# commodity_list = utils.get_commodity_list()
commodity_list = md.get_commodity_list()


tab1, tab2 = st.tabs(["Time Series Graph with Avg Prices", "Time Series Graph with Districts"])
with tab1:
    commodity = st.selectbox("Select Commodity", commodity_list, key="commodity_tab2")
    if st.button("Submit", key="submit_tab2"):
        data = mongo_dao.find_commodities(commodity=commodity)
        data = graph_display.process_data(data)

        st.plotly_chart(graph_display.time_series_graph_with_avg_prices(data))

with tab2:
    market_list = pd.read_csv("data/metadata/market_list.csv")['text'].tolist()
    market_list.sort()
    commodity = st.selectbox("Select Commodity", commodity_list, key="commodity_tab3")
    markets = st.multiselect(
        'Select Markets:',
        options=market_list,
        default=["Shajapur"],
        key="markets_tab3"
    )
    if st.button("Submit", key="submit_tab3"):
        data = mongo_dao.find_commodities(commodity=commodity)
        data = graph_display.process_data(data)
        filtered_df = data[data["Market Name"].isin(markets)]
        st.plotly_chart(graph_display.time_series_graph(filtered_df))
