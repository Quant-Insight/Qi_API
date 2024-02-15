#############################################################################################################################################################################################
# 
# get_model_sensitivities_paginated_one_day(target_date, models=models,tags=tags, asset_classes=asset_classes, term=term, model_count=model_count,exclusive_start_key=exclusive_start_key) 
# is a QI API endpoint to retrieve the sensitivities for multiple assets for a given date. Note that if the asset universe is large, it can take several minutes to pull 
# all asset sensitivities.  
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
#                 {'Model': 'A',
#                  'FinSub Credit': -0.38334,
#                  'Itraxx Japan': -0.32033,
#                  'Itraxx Xover': -0.47727,
#                  'JPY 10Y Real Rate': -0.06651,
#                  'USD 10Y Real Rate': -0.54041,
#                  'China 5Y CDS': -0.35719,
#                  'EM CDS': -0.25019,
#                  'Italian Sov. Confidence': -0.58794,
#                  'Copper': 0.48586,
#                  'Iron Ore': 0.43123,
#                  'VIX': 0.30648,
#                  'VXEEM': 0.3598,
#                  'USD Liquidity - EUR': 0.88494,
#                  'USD Liquidity - JPY': 0.64997,
#                  'VDAX': 0.27223,
#                  'US 10Y Infl. Expec.': -0.94378,
#                  'US 2Y Infl. Expec.': -0.65697,
#                  'US 5Y Infl. Expec.': -0.81722,
#                  'US 5s30s Swap': 0.6244,
#                  'USDCNH': -0.53109,
#                  'WTI': -0.44088,
#                  'US HY': -0.56051,
#                  'BoJ QT Expectations': -0.14789,
#                  'FED Rate Expectations': 0.08618,
#                ...
#                   }
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

# Function to process sensitivity data in the paginated response.
def process_sensitivity_response(response):
    results = []
    data = response['items']
    last_evaluated_key = response.get('last_evaluated_key', None)
    for model, model_data in data.items():
        for date, _model_data in model_data.items():
            result = {'Model': model}
            for sens_data in _model_data:
                result[sens_data['driver_short_name']] = sens_data['sensitivity']
        results.append(result)
    return results, last_evaluated_key

try:
    response = api_instance.get_model_sensitivities_paginated_one_day(
        target_date = target_date,
        asset_classes = asset_classes,
        tags = tags
    )
    results, exclusive_start_key = process_sensitivity_response(response)
    
    while exclusive_start_key:
        
        response = api_instance.get_model_sensitivities_paginated_one_day(
            target_date = target_date,
            asset_classes = asset_classes,
            tags = tags,
            exclusive_start_key = exclusive_start_key
        )
        _results, exclusive_start_key = process_sensitivity_response(response)
        results += _results

    df_results = pandas.DataFrame(results)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_model_sensitivities_paginated_one_day: %s\n" % e)
