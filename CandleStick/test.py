import pandas as pd
from datetime import datetime, timedelta, timezone



cron = pd.read_csv("cron.csv")

print(cron.head())

from_date = cron.loc[cron['name'] == "Wheat", 'last scrap date'].values[0]
from_date = datetime.strptime(from_date, '%Y-%m-%d')

print(type(from_date), from_date)