#######################################################################################################################################
# 
# get_model_sensitivities(model, date_from=date_from, date_to=date_to, term=term, numeric_id=numeric_id, version=version) is a QI API 
# function to retrieve the sensitivities of a given model within a given period of time (356 days max).  
# 
# Inputs:
#               * model - numeric id or name of the model (e.g. 'AAPL')
#               * date_from (optional) - begining of the period we want to retrieve (e.g. '2015-01-01')
#               * date_to (optional) - end of the period we want to retrieve (e.g. '2016-01-01')
#               * term (optional - we recommend to use 'Long Term'): 
#                                 * 'Long Term' is defined as 250 day lookback period.
#                                 * 'Short Term' is defined as 83 day lookback period.
#               * numeric_id (optional) - True to consider driver as a numeric id. False to consider driver as a name (False by default).
#               * version (optional) - version of the model in the API. 
#
# Output: Sensitivities of a given model during a giving period of time (356 days max).
#               * e.g.
#                      {'2015-01-01': [{'bucket_name': 'Global Growth',
#                                         'coefficient': ...,
#                                         'driver_contribution': None,
#                                         'driver_name': 'Euro GDP [...]',
#                                         'driver_short_name': 'Euro GDP',
#                                         'driver_zscore': None,
#                                         'driver_zscore_window_mean': None,
#                                         'driver_zscore_window_stdev': None,
#                                         'sensitivity': ...},
#                                        ],
#                                       ...
#                                       ...
#                         '2015-01-02': [{'bucket_name': 'Global Growth',
#                                         'coefficient': ...,
#                                         'driver_contribution': None,
#                                         'driver_name': 'Euro GDP [...]',
#                                         'driver_short_name': 'Euro GDP',
#                                         'driver_zscore': None,
#                                         'driver_zscore_window_mean': None,
#                                         ...
#                                         ...
#                        }
#
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
    api_response = api_instance.get_model_sensitivities(model, date_from=date_from, date_to=date_to, term=term, numeric_id=numeric_id, version=version)
    pprint(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_model_sensitivities: %s\n" % e)
