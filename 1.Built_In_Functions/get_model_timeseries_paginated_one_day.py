#############################################################################################################################################################################################
# 
# get_model_timeseries_paginated_one_day(target_date, models=models,tags=tags, asset_classes=asset_classes, term=term, model_count=model_count,exclusive_start_key=exclusive_start_key)
# is a QI API endpoint to retrieve the model data for multiple assets for a given date. Note that if the asset universe is large, it can take several minutes to pull 
# all asset model data.  
# 
# Inputs:
#               * target_date [date] (required) - Date of data required YYYY-MM-DD format.
#               * models[str] (optional) - Comma delimited string containing models with which to filter results.
#               * tags [str] (optional) - Comma delimited string containing tags with which to filter results. Results must contain all tags specified.
#               * asset_classes [str] (optional) - Comma-delimited list of asset classes with which to filter results. Results must contain any asset class specified.
#               * term [str] (optional) - Parameter of the models. We recommend using 'Long Term', which is the default if not set): 
#                                 * 'Long Term' is defined as a 250-day lookback period.
#                                 * 'Short Term' is defined as an 83-day lookback period.
#               * exclusive_start_key [str] (optional) - Key to use to denote the beginning of the page.
#               * model_count [int] (optional) - Maximum number of models for which data is returned (page count). 
#
# Output: Dictionary
#               * e.g.
#                    
#                {'A': {'2009-01-01': {'rsquare': 69.20703,
#                     'sigma': -0.42699,
#                     'percentage_gap': -19.86724,
#                     'fair_value': 12.06,
#                     'target_stdev': 4.6815,
#                     'absolute_gap': -1.99894,
#                     'target_mean': 18.88914,
#                     'target_zscore': -1.88564,
#                     'constant': -0.33145,
#                     'zscore': -1.45866}},
#                ...
#                  }
#                
#
#############################################################################################################################################################################################


from __future__ import print_function
import time
import qi_client
from qi_client.rest import ApiException
from pprint import pprint
import pandas

# Configure API key authorization: QI API Key
configuration = qi_client.Configuration()

# Add the API Key provided by QI
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'

# Uncomment to set up a proxy
# configuration.proxy = 'http://localhost:3128'

# create an instance of the API class
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))

# Setup parameters
asset_classes = 'Equity'
tags = 'USD, Stock'
target_date = '2024-02-14'

# Function to process timeseries data in the paginated response.
def process_timeseries_response(response, target_date):
    results = []
    data = response['items']
    last_evaluated_key = response.get('last_evaluated_key', None)
    for model, _model_data in data.items():
        result = {'Model': model}
        for _data in _model_data[target_date]:
                result[_data] = _model_data[target_date][_data]
        results.append(result)
    return results, last_evaluated_key

try:
    response = api_instance.get_model_timeseries_paginated_one_day(
        target_date = target_date,
        asset_classes = asset_classes,
        tags = tags
    )
    results, exclusive_start_key = process_timeseries_response(response, target_date)
    
    while exclusive_start_key:
        
        response = api_instance.get_model_timeseries_paginated_one_day(
            target_date = target_date,
            asset_classes = asset_classes,
            tags = tags,
            exclusive_start_key = exclusive_start_key
        )
        _results, exclusive_start_key = process_timeseries_response(response, target_date)
        results += _results
    
    df_results = pandas.DataFrame(results)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_model_sensitivities_paginated_one_day: %s\n" % e)
