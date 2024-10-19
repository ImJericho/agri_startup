import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import main




def display_candlestick_chart(file_path):
    df = pd.read_csv(file_path)
    fig = go.Figure(data=[go.Candlestick(x=df['formatted_date'],
                open=df['Modal Price (Rs./Quintal)'],
                high=df['Max Price (Rs./Quintal)'],
                low=df['Min Price (Rs./Quintal)'],
                close=df['Modal Price (Rs./Quintal)'])])
    # fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()



if __name__ == "__main__":
    commodities = main.find_all_commodities_of_intrest()
    for commodity in commodities:
        display_candlestick_chart(f"dataset/rawdata/{commodity}.csv")
