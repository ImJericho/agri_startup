import streamlit as st
import pandas as pd
import dao.mongo_dao as md
import plotly.express as px
import agrimarket
import gfinance
import main

st.title("Commodity Market Prices")

commodity_list = main.find_all_commodities_of_intrest()
mongo_dao = md.mongo_dao()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Candlestick Chart", "Time Series Graph ", "Time Series Graph with Avg Prices", "Comparison with Google Finance"])

with tab1:
    commodity = st.selectbox("Select Commodity", commodity_list, key="commodity_tab1")
    if st.button("Submit", key="submit_tab1"):
        data = mongo_dao.find_commodities(commodity=commodity)
        data = agrimarket.process_data(data)
        st.plotly_chart(agrimarket.candlestick_chart(data))

with tab3:
    commodity = st.selectbox("Select Commodity", commodity_list, key="commodity_tab2")
    if st.button("Submit", key="submit_tab2"):
        data = mongo_dao.find_commodities(commodity=commodity)
        data = agrimarket.process_data(data)

        st.plotly_chart(agrimarket.time_series_graph_with_avg_prices(data))

with tab2:
    market_list = pd.read_csv("dataset/metadata/market_list.csv")['text'].tolist()
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
        data = agrimarket.process_data(data)
        filtered_df = data[data["Market Name"].isin(markets)]
        st.plotly_chart(agrimarket.time_series_graph(filtered_df))


with tab4:
    commodity = st.selectbox("Select Commodity", commodity_list, key="commodity_tab4")
    if st.button("Submit", key="submit_tab4"):
        data = mongo_dao.find_commodities(commodity=commodity)
        data = agrimarket.process_data(data)
        data = data.groupby('formatted_date')['Modal Price'].mean().reset_index()
        data["Market Name"] = "Agrimarket"
        print("----------- agrimarket")
        print(data.head())
        try:
            gfinance_data = gfinance.get_data(commodity)
            gfinance_data.rename(columns={"Date": "formatted_date", "Close": "Modal Price"}, inplace=True)
            #concatenate gfinance_data to data
            data = pd.concat([data, gfinance_data], ignore_index=True)
            print("----------- gfinance")
            print(gfinance_data.head())
        except:
            print("No data available for the commodity in Google Finance")
            st.write("No data available for the commodity in Google Finance")

        st.plotly_chart(agrimarket.time_series_graph(data))