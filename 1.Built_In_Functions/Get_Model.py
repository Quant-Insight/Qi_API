#######################################################################################################################################
# 
# get_model(model, term, version, numeric_id) is a QI API function to retrieve the information of a given model.  
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
#                     {'asset_class': 'Equity',
#                      'created': None,
#                      'definition': {'bucket': None,
#                                     'expression': 'a',
#                                     'id': 5069,
#                                     'instrument1': {'coverage': None,
#                                                     'id': 30962,
#                                                     'mnemonic': 'PX_LAST',
#                                                     'ticker': '...'},
#                                     'instrument2': None,
#                                     'instrument3': None,
#                                     'instrument4': None},
#                        'drivers': [{'buckets': ['...'],
#                                     'expression': 'a',
#                                     'id': 1632,
#                                     'instrument1': {'coverage': None,
#                                                     'id': 23165,
#                                                     'mnemonic': 'PX_LAST',
#                                                     'ticker': '...'},
#                                     'instrument2': None,
#                                     'instrument3': None,
#                                     'instrument4': None,
#                                     'name': 'FinSub Credit [...]',
#                                     'short_name': 'FinSub Credit'},
#                         ...
#                         ...
#                         ...
#                         'id': 6857,
#                         'model_parameter': 'long term',
#                         'name': 'AAPL',
#                         'notes': '',
#                         'status': 'ACTIVE',
#                         'tags': ['S&P 1500'],
#                         'version': 1}
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

# Numeric ID or name of the model to retrieve
# Datatype: str
model = 'AAPL'

# Which model term to retrieve (optional)
# Datatype: str
term = 'Long Term'

# Which version of the model to retrieve data for. (optional)
# Datatype: int
version = 1

# If set to true, will consider identifier as a numeric ID - not as a name.(optional) (default to false)
# Datatype: bool
numeric_id = False

try:
    # Get a model definition
    api_response = api_instance.get_model(model, term=term, version=version, numeric_id=numeric_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_model: %s\n" % e)
