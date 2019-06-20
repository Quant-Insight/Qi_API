    
#######################################################################################################################################
# 
# get_driver(driver, numeric_id) is a QI API function to retrieve the information of a given driver.  
# 
# Inputs:
#               * driver - numeric id or name of the driver (e.g. 'Itraxx Japan')
#               * numeric_id (optional) - True to consider driver as a numeric id. False to consider driver as a name (False by default).
#
# Output: All the information of the requested driver.
#               * e.g.
#                      {'buckets': ['Corp credit'],
#                       'expression': 'a',
#                       'id': 1633,
#                       'instrument1': {'coverage': None,
#                                       'id': 23166,
#                                       'mnemonic': 'PX_LAST',
#                                       'ticker': '...'},
#                       'instrument2': None,
#                       'instrument3': None,
#                       'instrument4': None,
#                       'name': 'Itraxx Japan [...]',
#                       'short_name': 'Itraxx Japan'}
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

# Numeric ID or name of the driver to examine
# Datatype: str

driver = 'Itraxx Japan'

# If set to true, will consider identifier as a numeric ID - not as a name. (optional) (default to false)
# Datatype: bool

numeric_id = False

try:
    # Get driver details
    api_response = api_instance.get_driver(driver, numeric_id=numeric_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_driver: %s\n" % e)
