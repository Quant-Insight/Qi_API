#######################################################################################################################################
# 
# get_model_timeseries(model, date_from=date_from, date_to=date_to, term=term, numeric_id=numeric_id, version=version) is a QI API 
# function to retrieve the timeseries of a given model.  
# 
# Inputs:
#               * model - numeric id or name of the model (e.g. 'AAPL')
#               * term (optional - we recommend to use 'Long Term'): 
#                                 * 'Long Term' is defined as 250 day lookback period.
#                                 * 'Short Term' is defined as 83 dat lookback period.
#               * version (optional) - version of the model in the API. 
#               * numeric_id (optional) - True to consider driver as a numeric id. False to consider driver as a name (False by default).
#
# Output: All the information of the requested model.
#               * e.g.
#                     [{'_date': datetime.datetime(2015, 1, 1, 0, 0),
#                       'absolute_gap': ...,
#                       'constant': ...,
#                       'fair_value': ...,
#                       'percentage_gap': ...,
#                       'rsquare': ...,
#                       'sensitivities': None,
#                       'sigma': ...,
#                       'target_mean': ...,
#                       'target_stdev': ...,
#                       'target_zscore': ...,
#                       'zscore': ...},
#                       {'_date': datetime.datetime(2015, 1, 2, 0, 0),
#                         ...
#                         ...}
#                     ]
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

# Numeric ID or name of the model to retrieve sensitivities for
# Datatype: str
model = 'AAPL'

# Date in YYYY-MM-DD format from which to retrieve data (optional)
# Datatype: date
date_from = '2015-01-01'

# Date in YYYY-MM-DD format until which to retrieve data (optional)
# Datatype: date

date_to = '2016-01-01'
# Which model term to retrieve (optional)
# Datatype: str
term = 'Long Term'

# If set to true, will consider identifier as a numeric ID - not as a name.(optional) (default to false)
# Datatype: bool
numeric_id = False

# Which version of the model to retrieve data for. (optional)
# Datatype: int
version = 1

try:
    # Get sensitivities for a model
    api_response = api_instance.get_model_timeseries(model, date_from=date_from, date_to=date_to, term=term, numeric_id=numeric_id, version=version)
    pprint(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_model_sensitivities: %s\n" % e)
