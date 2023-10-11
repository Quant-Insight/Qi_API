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
#                        {'asset_class': 'Equity',
#                         'calc_complete': datetime.datetime(2023, 10, 11, 5, 33, 10, tzinfo=tzutc()),
#                         'created': None,
#                         'definition': {'bucket': None,
#                                        'expression': 'a',
#                                        'id': 314,
#                                        'timeseries_ety1': {'field': 'close',
#                                                            'id': 29,
#                                                            'instrument': {'asset_class': None,
#                                                                           'id': 31,
#                                                                           'identifiers': {'BloombergTicker': 'AAPL '
#                                                                                                              'US '
#                                                                                                              'Equity',
#                                                                                           'ISIN': 'US0378331005',
#                                                                                           'MSID': '126.1.AAPL',
#                                                                                           'SEDOL': '2046251'},
#                                                                           'is_future': False,
#                                                                           'name': 'AAPL',
#                                                                           'source': 'Morningstar',
#                                                                           'status': 'active'},
#                                                            'last_source': 'Morningstar',
#                                                            'status': 'active'},
#                                        'timeseries_ety2': None,
#                                        'timeseries_ety3': None,
#                                        'timeseries_ety4': None},
#                        ...
#                         'status': 'ACTIVE',
#                         'tags': ['S&P 500', 'Technology', 'USD', 'Stock'],
#                         'type': 'QI',
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
