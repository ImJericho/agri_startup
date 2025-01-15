import pandas as pd
from datetime import datetime
import logging
from service.writer_util import AgriDataCollector

def update_commodity_in_atlas(mongo_dao, commodity):
    collector = AgriDataCollector()
    cron = pd.read_csv("cron_data/cron.csv")
    market_list = pd.read_csv("cron_data/market_list.csv")

    if commodity in cron['name'].values:
        from_date = cron.loc[cron['name'] == commodity, 'last_scrap_date'].values[0]
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.now()
    else:
        return False
    logging.info(f"===called for {commodity}, {from_date}, {to_date}")

    for _, market in market_list.iterrows():
        data = collector.collect_rawdata(from_date, to_date, commodity, market['state'], market['district'], market['text'])
        mongo_dao.upsert_transactions(commodity, data)
        logging.info(f"Data uploaded for {commodity} for {market['text']}, and of size {data.shape}")

    # cron.loc[cron['name'] == commodity, 'last_scrap_date'] = to_date.strftime('%Y-%m-%d')
    # cron = cron.loc[:, ~cron.columns.str.contains('^Unnamed')]
    # cron.to_csv("cron_cata/cron.csv", index=False)

    logging.info(f"===Process Completed for {commodity}")
    return True
