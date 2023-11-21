#######################################################################################################################################
# 
# get_model_sensitivities_paginated_one_day(model, date_from=date_from, date_to=date_to, term=term, numeric_id=numeric_id, version=version) is a QI API 
# endpoint to retrieve the sensitivities for multiple models for given date.  
# 
# Inputs:
#               * asset_classes (optional) - asset class to filter assets by (e.g. 'Equity')
#               * tags (optional) - tag (sub category) to filter assets by (e.g. 'Stock' or 'USD' or 'S&P 500') 
#               * target_date (optional) - the date to request data for (e.g. '2023-11-17'), default is the previous week day (t-1)
#               * date_to (optional) - end of the period we want to retrieve (e.g. '2016-01-01')
#               * term (optional - we recommend to use 'Long Term', which is the default if not set): 
#                                 * 'Long Term' is defined as 250 day lookback period.
#                                 * 'Short Term' is defined as 83 day lookback period.
#               * exclusive_start_key (optional) - start key for pagination (use last_evaluated_key from previous paginated response).
#               * model_count (optional) - number of models to return in each paginated response (default is 100). 
#
# Output: Sensitivities of a given model during a giving period of time (356 days max).
#               * e.g.
#                    {'items': {'A': {'2023-11-17': [{'driver_name': 'FinSub Credit [{FinSub Credit | bid_spread}]',
#                         'driver_short_name': 'FinSub Credit',
#                         'bucket_name': 'Corporate Credit',
#                         'sensitivity': -0.1669},
#                        {'driver_name': 'Itraxx Japan [{iTraxx Japan | bid_spread}]',
#                         'driver_short_name': 'Itraxx Japan',
#                         'bucket_name': 'Corporate Credit',
#                         'sensitivity': -0.1309},
#                        {'driver_name': 'Itraxx Xover [{iTraxx Xover | bid_spread}]',
#                         'driver_short_name': 'Itraxx Xover',
#                         'bucket_name': 'Corporate Credit',
#                         'sensitivity': -0.17576},
#                        {'driver_name': 'JPY 10Y Real Rate [{JPY 10Y IL Govt. | yield_bid}]',
#                         'driver_short_name': 'JPY 10Y Real Rate',
#                         'bucket_name': 'Real Rates',
#                         'sensitivity': 2.88986},
#                    ...
#                    ... ]}}
#                    'model_count': 100,
#                    'last_evaluated_key': 'AIG'}
#
#######################################################################################################################################


from __future__ import print_function
import time
import qi_client
from qi_client.rest import ApiException
from pprint import pprint

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
        asset_classes='Equity',
        tags='USD, Stock'
    )
    results, exclusive_start_key = process_sensitivity_response(response)
    
    while exclusive_start_key:
        
        response = api_instance.get_model_sensitivities_paginated_one_day(
            asset_classes='Equity',
            tags='USD, Stock',
            exclusive_start_key=exclusive_start_key
        )
        _results, exclusive_start_key = process_sensitivity_response(response)
        results += _results
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_model_sensitivities_paginated_one_day: %s\n" % e)
