import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import main


def candlestick_chart(df, show_fig=False):
    fig = go.Figure(data=[go.Candlestick(x=df['formatted_date'],
                open=df['Modal Price'],
                high=df['Max Price'],
                low=df['Min Price'],
                close=df['Modal Price'])])
    # fig.update_layout(xaxis_rangeslider_visible=False)
    if show_fig:
        fig.show()
    return fig

def time_series_graph(df, show_fig=False):
    fig = px.line(df, x="formatted_date", y="Modal Price", title='Time Series', color='Market Name')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period")

    if show_fig:
        fig.show()
    return fig

def time_series_graph_with_avg_prices(df, show_fig=False):
    fig = px.line(df, x="formatted_date", y="Modal Price", title='Time Series', color='Market Name')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period")

    avg_price = df.groupby('formatted_date')['Modal Price'].mean().reset_index()
    fig.add_scatter(x=avg_price['formatted_date'], y=avg_price['Modal Price'], mode='lines', name='Average Price')
    if show_fig:
        fig.show()


    fig2 = px.line(x=avg_price['formatted_date'], y=avg_price['Modal Price'])

    return fig2

def process_data(data):
    df = pd.DataFrame(data)
    #sort df according to formatted_date
    df = df.sort_values(by='formatted_date')
    return df

if __name__ == "__main__":

    mongo_dao = md.mongo_dao()
    # data = mongo_dao.find_commodities(commodity="Garlic", start_date=datetime(2023, 1, 1), end_date=datetime(2024, 10, 1))
    data = mongo_dao.find_commodities(commodity="Garlic")
    df = process_data(data)

    # print(df.head())
    candlestick_chart(df, show_fig=True)
    time_series_graph(df, show_fig=True)



    # commodities = main.find_all_commodities_of_intrest()
    # for commodity in commodities:
    #     candlestick_chart(f"dataset/rawdata/{commodity}.csv")
