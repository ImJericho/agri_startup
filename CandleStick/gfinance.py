import pandas as pd



def get_data(commodity):
    soyabean = pd.read_csv(f'/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/gfinance/{commodity}.csv')
    soyabean['formatted_date'] = pd.to_datetime(soyabean['date'])
    soyabean["Modal Price"] = soyabean["value"] * 272/80
    # soyabean.drop(columns=["value"], inplace=True)
    soyabean['Market Name'] = "Soybean Continuous contract CBOT"
    return soyabean


if __name__ == "__main__":
    get_data("Soyabean")