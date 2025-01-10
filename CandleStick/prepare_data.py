import pandas as pd



def prepare_data():
    #read the raw_data.csv file and create a new csv file which will contain 3 columns: Date, High, Low such that high will be max price and low will be min price
    df = pd.read_csv('raw_data.csv')
    # df['Date'] = pd.to_datetime(df['Price Date'])
    # df['High'] = df[['AAPL.High', 'AAPL.Open', 'AAPL.Close']].max(axis=1)
    # df['Low'] = df[['AAPL.Low', 'AAPL.Open', 'AAPL.Close']].min(axis=1)
    # df = df[['Date', 'High', 'Low']]
    

    df['formatted_date'] = pd.to_datetime(df['Price Date'], format='%d %b %Y')
    df['formatted_date'] = df['formatted_date'].dt.strftime('%d-%m-%Y')
    df.to_csv('prepared_data.csv', index=False)



if __name__ == '__main__':
    prepare_data()