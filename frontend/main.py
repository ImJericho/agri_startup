import streamlit as st
import pandas as pd
import mongo_dao as md
import graph_display as graph_display
import utils
from datetime import datetime
import backend

st.set_page_config(
    page_title="Crop Market Prices",
    page_icon=":seedling:",
)

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :seedling: Crop Market Prices Dashboard

Welcome to the Crop Market Prices Dashboard. Here you can explore and analyze the market prices of various crops over time.
'''

# Add some spacing
''
''

mongo_dao = md.mongo_dao()
min_date = 2020
max_date = 2025

# commodity_list = utils.get_commodity_list()
commodity_list = mongo_dao.get_commodity_list()


tab1, tab2, tab3 = st.tabs(["Time Series Graph with Avg Prices", "Time Series Graph with Districts", "Update Data in Atlas"])
with tab1:
    commodity = st.selectbox("Select Commodity", commodity_list, key="commodity_tab2")
    from_year, to_year = st.slider(
        'Which year are you interested in?',
        key="date_slider_tab1",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],    
    )
    start_date = datetime(from_year, 1, 1)
    end_date = datetime(to_year, 12, 31)

    if st.button("Submit", key="submit_tab2"):
        data = mongo_dao.find_commodities(commodity=commodity, start_date=start_date, end_date=end_date)
        data = graph_display.process_data(data)

        st.plotly_chart(graph_display.time_series_graph_with_avg_prices(data))

with tab2:
    market_list = pd.read_csv("frontend/data/metadata/market_list.csv")['text'].tolist()
    market_list.sort()
    commodity = st.selectbox("Select Commodity", commodity_list, key="commodity_tab3")
    markets = st.multiselect(
        'Select Markets:',
        options=market_list,
        default=["Shajapur"],
        key="markets_tab3"
    )
    from_year, to_year = st.slider(
        'Which year are you interested in?',
        key="date_slider_tab2",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],    
    )
    start_date = datetime(from_year, 1, 1)
    end_date = datetime(to_year, 12, 31)
    if st.button("Submit", key="submit_tab3"):
        data = mongo_dao.find_commodities(commodity=commodity, start_date=start_date, end_date=end_date)
        data = graph_display.process_data(data)
        filtered_df = data[data["Market Name"].isin(markets)]
        st.plotly_chart(graph_display.time_series_graph(filtered_df))


with tab3:
    market_list = pd.read_csv("backend/data/metadata/market_list.csv")
    cron_job = pd.read_csv("backend/cron.csv")
    commodities =utils.get_commodity_list()

    st.write("### Update Data in Atlas")

    # Create a DataFrame for displaying commodities with a serial number
    commodities_df = pd.DataFrame({
        "S.No": range(1, len(commodities) + 1),
        "Commodity": commodities
    })

    # Display the table with a button in the third column
    for index, row in commodities_df.iterrows():
        col1, col2, col3 = st.columns([1, 3, 1])
        col1.write(row["S.No"])
        col2.write(row["Commodity"])
        if col3.button("Update", key=f"update_{index}"):
            done = backend.process_commodity(row["Commodity"], cron_job, market_list)
            if done:
                st.success(f"Update for {row['Commodity']} is complete.")
            else:
                st.error(f"Update for {row['Commodity']} failed.")