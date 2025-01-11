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
    st.header('Price over time', divider='gray')
    st.write('This graph shows average price of crop in all the markets over time.')
    ''
    commodity = st.selectbox("Select Crop", commodity_list, key="commodity_tab2")
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
        success = False
        try:
            data = graph_display.process_data(data)
            success = True
        except:
            st.error("No data found for the selected crop.")


        if success:
            st.plotly_chart(graph_display.time_series_graph_with_avg_prices(data, show_fig=False, sunday=False))
            ''
            ''

            st.header(f"Compare from history for {commodity}", divider=True)
            tz = utils.TimeDataHandler()
            from_date, to_date = tz.date_range_for_today()
            today_price = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            today_price = graph_display.get_average_price(today_price)

            from_date, to_date = tz.date_range_for_past_x_weeks(1)
            week_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            week_avg_price = graph_display.get_average_price(week_data, sunday=False)

            from_date, to_date = tz.date_range_for_past_x_months(1)
            month_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            month_avg_price = graph_display.get_average_price(month_data, sunday=False)

            from_date, to_date = tz.date_range_for_past_x_months(3)
            quarter_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            quarter_avg_price = graph_display.get_average_price(quarter_data, sunday=False)

            from_date, to_date = tz.date_range_for_past_x_years(1)
            year_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            year_avg_price = graph_display.get_average_price(year_data, sunday=False)

            avg_price_data = {
                'week': week_avg_price,
                'month': month_avg_price,
                'quarter': quarter_avg_price,
                'year': year_avg_price
            }
            st.metric(
                label=f"Today's Price",
                help=f"Date ({datetime.now().strftime('%Y-%m-%d %A')})",
                value=f'{today_price}₹',
                border=True,
            )

            cols = st.columns(2)
            for i, period in enumerate(['week', 'month', 'quarter', 'year']):
                col = cols[i % len(cols)]
            
                with col:
                    avg_price = avg_price_data[period]
                    avg_price_display = f'{avg_price:,.2f}'             
                    growth = f'{((week_avg_price - avg_price) / avg_price) * 100:.2f}%'

                    st.metric(
                        label=f"This {period.capitalize()}'s AVG Price",
                        value=f'{avg_price_display}₹',
                        delta=growth,
                        border=True,
                    )

with tab2:
    st.header('Price over time', divider='gray')
    st.write('This graph shows market wise price of crop.')

    ''
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
        success = False
        try:
            data = graph_display.process_data(data)
            data = data[data["Market Name"].isin(markets)]
            success = True
        except:
            st.error("No data found for the selected crop.")
        
        if success:
            sunday = False
            st.plotly_chart(graph_display.time_series_graph(data, show_fig=False, sunday=sunday))
            ''
            ''

            st.header(f"Compare from history for {commodity}", divider=True)
            tz = utils.TimeDataHandler()
            from_date, to_date = tz.date_range_for_today()
            today_price = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            today_price = graph_display.get_average_price_for_given_markets(today_price, markets)

            from_date, to_date = tz.date_range_for_past_x_weeks(1)
            week_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            week_avg_price = graph_display.get_average_price_for_given_markets(week_data, sunday=sunday, markets=markets)

            from_date, to_date = tz.date_range_for_past_x_months(1)
            month_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            month_avg_price = graph_display.get_average_price_for_given_markets(month_data, sunday=sunday, markets=markets)

            from_date, to_date = tz.date_range_for_past_x_months(3)
            quarter_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            quarter_avg_price = graph_display.get_average_price_for_given_markets(quarter_data, sunday=sunday, markets=markets)

            from_date, to_date = tz.date_range_for_past_x_years(1)
            year_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
            year_avg_price = graph_display.get_average_price_for_given_markets(year_data, sunday=sunday, markets=markets)

            avg_price_data = {
                'week': week_avg_price,
                'month': month_avg_price,
                'quarter': quarter_avg_price,
                'year': year_avg_price
            }
            st.metric(
                label=f"Today's Price",
                help=f"Date ({datetime.now().strftime('%Y-%m-%d %A')})",
                value=f'{today_price}₹',
                border=True,
            )

            cols = st.columns(2)
            for i, period in enumerate(['week', 'month', 'quarter', 'year']):
                col = cols[i % len(cols)]
            
                with col:
                    avg_price = avg_price_data[period]
                    avg_price_display = f'{avg_price:,.2f}'             
                    growth = f'{((week_avg_price - avg_price) / avg_price) * 100:.2f}%'

                    st.metric(
                        label=f"This {period.capitalize()}'s AVG Price",
                        value=f'{avg_price_display}₹',
                        delta=growth,
                        border=True,
                    )


with tab3:
    market_list = pd.read_csv("frontend/data/metadata/market_list.csv")
    cron_job = pd.read_csv("frontend/cron.csv")
    commodities =utils.get_commodity_list()

    st.header("Update Data in Atlas", divider='gray')
    ''

    password = st.text_input("Enter Password", type="password")
    if password != "vivek-agri":
        st.warning("Incorrect password. Please try again.")
    else:
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