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

def time_series_graph(df, show_fig=False, sunday=True):
    if sunday==False:
        df['new_formatted_date'] = pd.to_datetime(df['formatted_date'])
        df = df[df['new_formatted_date'].dt.weekday != 6]
    
    fig = px.line(x=df["formatted_date"], y=df["Modal Price"], color='Market Name')
    fig.update_layout(
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )

    if show_fig:
        fig.show()
    return fig

def time_series_graph_with_avg_prices(df, show_fig=False, sunday=True):
    if sunday==False:
        df['new_formatted_date'] = pd.to_datetime(df['formatted_date'])
        df = df[df['new_formatted_date'].dt.weekday != 6]
    avg_price = df.groupby('formatted_date')['Modal Price'].mean().reset_index()

    fig = px.line(avg_price, x='formatted_date', y='Modal Price')
    fig.update_layout(
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    return fig

def get_average_price(df, sunday=True):
    df = pd.DataFrame(df)
    if len(df) == 0:
        return None
    if sunday==False:
        df['new_formatted_date'] = pd.to_datetime(df['formatted_date'])
        df = df[df['new_formatted_date'].dt.weekday != 6]
    return df['Modal Price'].mean()

def get_average_price_for_given_markets(df, markets, sunday=True):
    df = pd.DataFrame(df)
    try:
        df = df[df["Market Name"].isin(markets)]
        if sunday==False:
            df['new_formatted_date'] = pd.to_datetime(df['formatted_date'])
            df = df[df['new_formatted_date'].dt.weekday != 6]
        return df['Modal Price'].mean()
    except:
        return None


def process_data(data):
    df = pd.DataFrame(data)
    df = df.sort_values(by='formatted_date')
    return df

if __name__ == "__main__":
    pass