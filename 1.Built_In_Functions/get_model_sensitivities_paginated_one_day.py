#######################################################################################################################################
# 
# get_model_sensitivities_paginated_one_day(model, date_from=date_from, date_to=date_to, term=term, numeric_id=numeric_id, version=version) is a QI API 
# endpoint to retrieve the sensitivities for multiple assets for given date. Note that if the asset universe is large, it can take several minutes to pull 
# all asset's sensitivities.  
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
# Output: Pandas DataFrame of sensitivity data for a universe of assets for a given date.
#               * e.g.
#                    
#
#        model     | China GDP                   | China 5y CDS                        | Copper                | FinSub Credit                | ... | 
#       AAPL       | -0.26924                    | -0.26444                            | 0.31652               | 0.16956                      | ... |  
#       META       | -0.27617                    | -0.27528                            | 0.32443               | 0.15854                      | ... |  
#       AMZN       | -0.28721                    | -0.29178                            | 0.33853               | 0.15243                      | ... |  
#       ...        | ...                         | ...                                 | ...                   | ...                          | ... |       
#
#
#######################################################################################################################################


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

    df_results = pandas.DataFrame(results
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_model_sensitivities_paginated_one_day: %s\n" % e)
