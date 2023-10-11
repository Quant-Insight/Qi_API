#######################################################################################################################################
# 
# get_instrument(instrument, mnemonic=mnemonic, numeric_id=numeric_id)) is a QI API function to retrieve the information of a given 
# instrument.  
# 
# Inputs:
#               * instrument - numeric id or name of the instrument (e.g. 'AAPL')
#               * numeric_id (optional) - True to consider driver as a numeric id. False to consider driver as a name (False by default).
#
# Output: All the information of the requested instrument.
#               * e.g.
#                      {'asset_class': None,
#                         'id': 31,
#                         'identifiers': {'BloombergTicker': 'AAPL US Equity',
#                                         'ISIN': 'US0378331005',
#                                         'MSID': '126.1.AAPL',
#                                         'SEDOL': '2046251'},
#                         'is_future': False,
#                         'name': 'AAPL',
#                         'source': 'Morningstar',
#                         'status': 'active'}
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

# Numeric ID or name of the instrument to retrieve
# Datatype: str
instrument = 'AAPL'

# If set to true, will consider identifier as a numeric ID - not as a name.(optional) (default to false)
# Datatype: bool
numeric_id = False

try:
    # Get instrument definition
    api_response = api_instance.get_instrument(instrument, mnemonic=mnemonic, numeric_id=numeric_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_instrument: %s\n" % e)

