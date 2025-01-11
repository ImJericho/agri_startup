import pandas as pd
from datetime import datetime, timedelta, timezone


def get_commodity_list():
    commodity = pd.read_csv("frontend/data/metadata/commodity_of_intrest.csv")
    commodity_list = []
    for i in range(len(commodity)):
        commodity_list.append(commodity['Name'][i])
        # commodity_list.append(f"{commodity['Name'][i]}+'({commodity['display_name'][i]}")
    print(commodity_list)
    return commodity_list



class TimeDataHandler:
    def __init__(self):
        self.IST = timezone(timedelta(hours=5, minutes=30))

    def date_range_for_today(self):
        to_date = datetime.now(self.IST).date()
        from_date = to_date
        #convert to datetime object
        to_date = datetime.combine(to_date, datetime.min.time())
        from_date = datetime.combine(from_date, datetime.min.time())
        return from_date, to_date

    def date_range_for_past_x_days(self, x):
        to_date = datetime.now(self.IST).date()
        from_date = to_date - timedelta(days=x)
        #convert to datetime object
        to_date = datetime.combine(to_date, datetime.min.time())
        from_date = datetime.combine(from_date, datetime.min.time())
        return from_date, to_date

    def date_range_for_past_x_months(self, x):
        to_date = datetime.now(self.IST).date()
        from_date = to_date - timedelta(days=x*30)
        #convert to datetime object
        to_date = datetime.combine(to_date, datetime.min.time())
        from_date = datetime.combine(from_date, datetime.min.time())
        return from_date, to_date

    def date_range_for_past_x_years(self, x):
        to_date = datetime.now(self.IST).date()
        from_date = to_date - timedelta(days=x*365)
        #convert to datetime object
        to_date = datetime.combine(to_date, datetime.min.time())
        from_date = datetime.combine(from_date, datetime.min.time())
        return from_date, to_date

    def date_range_for_past_x_weeks(self, x):
        to_date = datetime.now(self.IST).date()
        from_date = to_date - timedelta(days=x*7)
        #convert to datetime object
        to_date = datetime.combine(to_date, datetime.min.time())
        from_date = datetime.combine(from_date, datetime.min.time())
        return from_date, to_date
