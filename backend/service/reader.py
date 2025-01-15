from service.time_util import TimeDataHandler
from service.utils import get_average_price
from datetime import datetime
import pandas as pd

def get_analysis(commodity, mongo_dao, markets=None, sunday=False):
    tz = TimeDataHandler()

    from_date, to_date = tz.date_range_for_today()
    today_price = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
    today_price = get_average_price(today_price, sunday=sunday, markets=markets)

    from_date, to_date = tz.date_range_for_past_x_weeks(1)
    week_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
    week_avg_price = get_average_price(week_data, sunday=sunday, markets=markets)

    from_date, to_date = tz.date_range_for_past_x_months(1)
    month_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
    month_avg_price = get_average_price(month_data, sunday=sunday, markets=markets)

    from_date, to_date = tz.date_range_for_past_x_months(3)
    quarter_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
    quarter_avg_price = get_average_price(quarter_data, sunday=sunday, markets=markets)

    from_date, to_date = tz.date_range_for_past_x_years(1)
    year_data = mongo_dao.find_commodities_prices(commodity=commodity, start_date=from_date, end_date=to_date)
    year_avg_price = get_average_price(year_data, sunday=sunday, markets=markets)

    analysis = {
        'today':{
            'avg_price': today_price,
            'growth': None
        },
        'week':{
            'avg_price': week_avg_price,
            'growth': ((today_price - week_avg_price) / week_avg_price) * 100 if today_price != None else None
        },
        'month':{
            'avg_price': month_avg_price,
            'growth': ((week_avg_price - month_avg_price) / month_avg_price) * 100 if week_avg_price != None else None
        },
        'quarter':{
            'avg_price': quarter_avg_price,
            'growth': ((month_avg_price - quarter_avg_price) / quarter_avg_price) * 100 if week_avg_price != None else None
        },
        'year':{
            'avg_price': year_avg_price,
            'growth': ((quarter_avg_price - year_avg_price) / year_avg_price) * 100 if week_avg_price != None else None
        }
    }

    return analysis



def get_graph_yearwise(commodity, mongo_dao, from_year, to_year, markets=None, sunday=False):
    start_date = datetime(from_year, 1, 1)
    end_date = datetime(to_year, 12, 31)
    data = mongo_dao.find_commodities(commodity, start_date, end_date)
    df = pd.DataFrame(data)
    df = df.sort_values(by='formatted_date')
    df = df[df["Market Name"].isin(markets)] if markets else df
    df = df[df["formatted_date"].dt.dayofweek == 6] if sunday else df
    df['formatted_date'] = df['formatted_date'].dt.strftime('%Y-%m-%d')
    print(f"Data size for graph: {len(df)}")
    json_data = df.to_json(orient ='records')
    return json_data


def get_commodities_list(mongo_dao):
    data = mongo_dao.get_commodities_list()
    return data


