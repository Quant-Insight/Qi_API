#######################################################################################################################################
# 
# This python script generates a csv file containing the most recent day's data.
#
# Run the following command in your terminal to generate the file:
#       python Pull_Latest_Data_To_csv.py --key "Your_API-KEY”
#
# The asset universe is defined as such in the script:
#   US = [x.name for x in api_instance.get_models(tags = 'S&P 1500')][::2]
#   Europe = [x.name for x in api_instance.get_models(tags = 'STOXX Europe 600')][::2]
#   ETFs = [x.name for x in api_instance.get_models(tags = 'ETF-Equity')][::2]
#   Indices = [x.name for x in api_instance.get_models(tags = 'Indices')][::2]
#   assets = US + Europe + ETFs + Indices
#
# However this can easily be altered to your specific assets, for example:
#   assets = ['AAPL','FB','MSFT','GS' ... ]
#
# 2 csv files will be generated, 1 for long term and 1 for short term, with the following format:
#   'Qi Data - Short Term_YYYY-mm-dd.csv' & 'Qi Data - Long Term_YYYY-mm-dd.csv'
#
# Both files contain a row per asset, with the following column headers:
#   •	FVG
#   •	Rsq
#   •	Model Value
#   •	Percentage Gap
#   •	Absolute Gap
#   •	Each individual driver with its sensitivities. 
#
#######################################################################################################################################


from __future__ import print_function 
import time
import qi_client
from qi_client.rest import ApiException
from pprint import pprint
import pandas
from datetime import datetime,timedelta
import argparse
import logging

configuration = qi_client.Configuration() 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-k', '--key', default=None,
                            help="API KEY, e.g. 'AS7TYesif9974HGDS72846hfIN98FD'.")
else:
    raise RuntimeError("Script may only be run directly.")

# Script entry point - parse input arguments.
arguments = arg_parser.parse_args()

### Input API Key

configuration.api_key['X-API-KEY'] = arguments.key
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed # configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# create an instance of the API class
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))


### Find last trading day

if datetime.today().weekday() == 0:
    date = datetime.now() - timedelta(3)
# apf: If today is Sunday, we retrieve data from previous Friday. 
elif datetime.today().weekday() == 6:
    date = datetime.now() - timedelta(2)
# apf: otherwise, we retrieve data from the previous day. 
else:
    date = datetime.now() - timedelta(1)
    
last_date = str(date)[:10]


### Function to pull sensitivity data

def get_sensitivity_grid(model,start,end,term):
    
    
    year_start = int(start[:4])
    year_end = int(end[:4])
    sensitivity = {}
    for year in range(year_start, year_end + 1):
        query_start = start
        
        if year != year_start:
            date_from = '%d-01-01' % year
        else:
            date_from = start
        if year != year_end:
            date_to = '%d-12-31' % year
        else:
            date_to = end
    
#         print("Gathering data for %s from %s to %s..." % (model,
#         date_from,
#         date_to))
    
        sensitivity.update(
        api_instance.get_model_sensitivities(model=model,date_from=date_from,date_to=date_to,term=term))
    
    
    df_sensitivities = pandas.DataFrame()
    sensitivity_grid = pandas.DataFrame()
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:
            df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = pandas.concat([sensitivity_grid, df_sensitivities], axis = 0, join = 'outer')

            
    return sensitivity_grid


### Function to pull model timeseries data

def get_model_data(model,start,end,term):
    
    
    year_start = int(start[:4])
    year_end = int(end[:4])
    time_series = []
    for year in range(year_start, year_end + 1):
        query_start = start
        
        if year != year_start:
            date_from = '%d-01-01' % year
        else:
            date_from = start
        if year != year_end:
            date_to = '%d-12-31' % year
        else:
            date_to = end
    
#         print("Gathering data for %s from %s to %s..." % (model,
#         date_from,
#         date_to))
    
        time_series += api_instance.get_model_timeseries(model=model,date_from=date_from,date_to=date_to,term=term)
    

    FVG = [data.sigma for data in time_series]
    Rsq = [data.rsquare for data in time_series]
    dates = [data._date for data in time_series]
    
    model_value = [data.fair_value for data in time_series]
    percentage_gap = [data.percentage_gap for data in time_series]
    absolute_gap = [data.absolute_gap for data in time_series]



    df_ = pandas.DataFrame({'FVG':FVG, 'Rsq':Rsq, 'Model Value':model_value, 'Percentage Gap':percentage_gap,
                            'Absolute Gap':absolute_gap})
    df_.index = dates
    
    return df_


### Define universe for Global Equities

US = [x.name for x in api_instance.get_models(tags = 'S&P 500')][::2]
Europe = [x.name for x in api_instance.get_models(tags = 'Euro Stoxx 600')][::2]
ETFs = [x.name for x in api_instance.get_models(tags = 'ETF-Equity')][::2]
Indices = [x.name for x in api_instance.get_models(tags = 'Indices')][::2]

assets = US + Europe + ETFs + Indices

### Pull data and export to csv

for term in ['Short Term','Long Term']:

    final_df = pandas.DataFrame()


    for asset in assets:

        try:

            model_data = get_model_data(asset,last_date,last_date,term)
            sens_data = get_sensitivity_grid(asset,last_date,last_date,term)

            combined_df = pandas.concat([model_data,sens_data], axis=1)
            combined_df.index = [asset]

            if final_df.empty:
                final_df = combined_df

            else:
                final_df = pandas.concat([final_df, combined_df], axis = 0, join = 'outer')

            print(str(assets.index(asset)+1) + '/' + str(len(assets)) + ' ' + term)

        except:
            pass
        
    final_df.to_csv('Qi Data - ' + term + '_' + last_date +'.csv')
