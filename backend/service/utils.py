import pandas as pd
import logging


def get_average_price(df, markets=None, sunday=True):
    df = pd.DataFrame(df)    
    if len(df) == 0:
        logging.debug("Dataframe is empty")
        return None
    if markets is None:
        logging.debug("No specific markets provided")
        if len(df) == 0:
            logging.debug("Dataframe is empty")
            return None
        if not sunday:
            logging.debug("Excluding Sundays from the data")
            df['new_formatted_date'] = pd.to_datetime(df['formatted_date'])
            df = df[df['new_formatted_date'].dt.weekday != 6]
        average_price = df['Modal Price'].mean()
        logging.debug(f"Calculated average price: {average_price}")
        return average_price
    
    else:
        print(f"Columns in dataframe: {df.columns.tolist()}")
        logging.debug(f"Columns in dataframe: {df.columns.tolist()}")
        print(f"Filtering dataframe for markets: {markets}")
        df = df[df['Market Name'].isin(markets)]
        if not sunday:
            logging.debug("Excluding Sundays from the data")
            df['new_formatted_date'] = pd.to_datetime(df['formatted_date'])
            df = df[df['new_formatted_date'].dt.weekday != 6]
        average_price = df['Modal Price'].mean()
        logging.debug(f"Calculated average price: {average_price}")
        return average_price