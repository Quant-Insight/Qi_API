#######################################################################################################################################
# 
# get_instruments() is a QI API function to retrieve all the instruments available in our API.  
# 
# Inputs
#               
# Output: A list with the coverage, id, mnemonic, and ticker of all the instruments available in our API.
#               * e.g.
#                       [{'asset_class': None,
#                         'id': 1,
#                         'identifiers': {},
#                         'is_future': False,
#                         'name': 'GDP Now-Cast Brazil',
#                         'source': 'Now-Casting',
#                         'status': 'active'},
#                         {'asset_class': None,
#                         'id': 2,
#                         'identifiers': {},
#                         'is_future': False,
#                         'name': 'GDP Now-Cast Canada',
#                         'source': 'Now-Casting',
#                         'status': 'active'},
#                         {'asset_class': None,
#                         'id': 3,
#                         'identifiers': {},
#                         'is_future': False,
#                         'name': 'GDP Now-Cast China',
#                         'source': 'Now-Casting',
#                         'status': 'active'},
#                         {'asset_class': None,
#                         'id': 4,
#                         'identifiers': {},
#                         'is_future': False,
#                        ...
#                         'is_future': False,
#                         'name': 'ITA',
#                         'source': 'Morningstar',
#                         'status': 'active'}]
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

try:
    # Get all instruments defined
    api_response = api_instance.get_instruments()
    pprint(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_instruments: %s\n" % e)
    
