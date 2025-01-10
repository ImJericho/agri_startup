import data_collectors.rawdata_collection as rdc
from datetime import datetime, timedelta, timezone
import pandas as pd
import mongo_dao
import logging
import utils
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_commodity(commodity, cron, market_list):
    mongo_client = mongo_dao.mongo_dao()
    collector = rdc.AgriDataCollector()

    if commodity in cron['name'].values:
        from_date = cron.loc[cron['name'] == commodity, 'last_scrap_date'].values[0]
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.now()
    else:
        from_date = datetime.strptime('2025-01-01', '%Y-%m-%d')
        to_date = datetime.now()
        new_row = pd.DataFrame([{'sno': len(cron)+1, 'name': commodity, 'type': 'commodity', 'first_scrap_date': from_date, 'active': 1}])
        cron = pd.concat([cron, new_row], ignore_index=True)
    logging.info(f"===called for {commodity}, {from_date}, {to_date}")

    with ThreadPoolExecutor() as executor:
        futures = []
        for _, market in market_list.iterrows():
            futures.append(executor.submit(collector.collect_rawdata, from_date, to_date, commodity, market['state'], market['district'], market['text']))
        for future in as_completed(futures):
            data = future.result()
            utils.upsert_data_atlas(mongo_client, commodity, data)
        # logging.info(f"Data uploaded for {commodity} for {market['text']}, and of size {data.shape}")

    # for _, market in market_list.iterrows():
    #     data = collector.collect_rawdata(from_date, to_date, commodity, market['state'], market['district'], market['text'])
    #     utils.upsert_data_atlas(mongo_client, commodity, data)
    #     logging.info(f"Data uploaded for {commodity} for {market['text']}, and of size {data.shape}")

    cron.loc[cron['name'] == commodity, 'last_scrap_date'] = to_date.strftime('%Y-%m-%d')
    cron = cron.loc[:, ~cron.columns.str.contains('^Unnamed')]
    cron.to_csv("backend/cron.csv", index=False)

    logging.info(f"===Process Completed for {commodity}")

if __name__ == "__main__":

    market_list = pd.read_csv("backend/data/metadata/market_list.csv")
    cron_job = pd.read_csv("backend/cron.csv")
    commodities = utils.find_all_commodities_of_interest()
    new_commodities = []
    for commodity in commodities:
        if cron_job.loc[cron_job['name'] == commodity, 'active'].values[0] == 1:
            if datetime.now().strftime('%Y-%m-%d') == cron_job.loc[cron_job['name'] == commodity, 'last_scrap_date'].values[0]:
                logging.info(f"Already scrapped till today for {commodity}. Skipping")
            else:               
                new_commodities.append(commodity) 

    print(f"commodities to be updated:{new_commodities}")   

    with ProcessPoolExecutor() as executor:
        results = executor.map(process_commodity, new_commodities, [cron_job]*len(new_commodities), [market_list]*len(new_commodities))
        print("===Process Submitted")
        for result in results:
            print(result)
