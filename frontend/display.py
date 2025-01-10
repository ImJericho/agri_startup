import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


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

def process_data(data):
    df = pd.DataFrame(data)
    #sort df according to formatted_date
    df = df.sort_values(by='formatted_date')
    return df
