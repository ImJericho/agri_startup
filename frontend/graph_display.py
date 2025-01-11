import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st



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
    fig = px.line(df, x="formatted_date", y="Modal Price", color='Market Name')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period")

    if show_fig:
        fig.show()
    return fig

def time_series_graph_with_avg_prices(df, show_fig=False):
    fig = px.line(df, x="formatted_date", y="Modal Price", color='Market Name')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period")
    
    df['new_formatted_date'] = pd.to_datetime(df['formatted_date'])
    df = df[df['new_formatted_date'].dt.weekday != 6]

    avg_price = df.groupby('formatted_date')['Modal Price'].mean().reset_index()
    fig.add_scatter(x=avg_price['formatted_date'], y=avg_price['Modal Price'], mode='lines', name='Average Price')
    if show_fig:
        fig.show()

    fig2 = px.line(x=avg_price['formatted_date'], y=avg_price['Modal Price'])
    return fig2

def get_average_price(df, sunday=True):
    df = pd.DataFrame(df)
    if sunday==False:
        df['new_formatted_date'] = pd.to_datetime(df['formatted_date'])
        df = df[df['new_formatted_date'].dt.weekday != 6]
    return df['Modal Price'].mean()

def process_data(data):
    df = pd.DataFrame(data)
    df = df.sort_values(by='formatted_date')
    return df

if __name__ == "__main__":
    pass