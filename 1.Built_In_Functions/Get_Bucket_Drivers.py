#######################################################################################################################################
# 
# get_bucket_drivers(bucket, numeric_id) is a QI API function to retrieve all the drivers .  
# 
# Inputs:
#               * bucket - numeric id or name of the bucket (e.g. 'Corp credit')
#               * numeric_id (optional) - True to consider bucket as a numeric id. False to consider bucket as a name (False by default).
#
# Output: A list with all the drivers of the bucket requested.
#               * e.g.
#                      [{'buckets': ['Corp credit'],
#                        'expression': 'a',
#                        'id': 1632,
#                        'instrument1': {'coverage': None,
#                                        'id': 23165,
#                                        'mnemonic': 'PX_LAST',
#                                        'ticker': '...'},
#                         'instrument2': None,
#                         'instrument3': None,
#                         'instrument4': None,
#                         'name': 'FinSub Credit [...]',
#                         'short_name': 'FinSub Credit'},
#                         ...
#                         ...
#                       ]
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

# Numeric ID or name of the bucket to examine
# Datatype: str

bucket = 'Corporate Credit'

# If set to true, will consider identifier as a numeric ID - not as a name. (optional) (default to false)
# Datatype: bool

numeric_id = False

try:
    # Get drivers for a given bucket
    api_response = api_instance.get_bucket_drivers(bucket, numeric_id=numeric_id)
    pprint(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_bucket_drivers: %s\n" % e)
    
