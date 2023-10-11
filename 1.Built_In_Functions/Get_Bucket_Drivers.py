#######################################################################################################################################
# 
# get_bucket_drivers(bucket, numeric_id) is a QI API function to retrieve all the drivers.  
# 
# Inputs:
#               * bucket - numeric id or name of the bucket (e.g. 'Corporate Credit')
#               * numeric_id (optional) - True to consider bucket as a numeric id. False to consider bucket as a name (False by default).
#
# Output: A list with all the drivers of the bucket requested.
#               * e.g.
#                      [{'buckets': ['Corporate Credit'],
#                        'deactivated': None,
#                        'expression': 'a',
#                         'id': 1,
#                         'name': 'FinSub Credit [{FinSub Credit | bid_spread}]',
#                         'short_name': 'FinSub Credit',
#                         'status': 'ACTIVE',
#                         'timeseries_ety1': {'field': 'bid_spread',
#                                             'id': 3736,
#                                             'instrument': {'asset_class': None,
#                                                            'id': 4150,
#                                                            'identifiers': {'BloombergTicker': 'ITRXEUE '
#                                                                                               'CBGT '
#                                                                                               'Index',
#                                                                            'IHSID': 'FinSub credit'},
#                                                            'is_future': False,
#                                                            'name': 'FinSub credit',
#                                                            'source': 'Ihsmarkit',
#                                                            'status': 'active'},
#                                             'last_source': 'Ihsmarkit',
#                                             'status': 'active'},
#                         'timeseries_ety2': None,
#                         'timeseries_ety3': None,
#                         'timeseries_ety4': None},
#                         {'buckets': ['Corporate Credit'],
#                        ...
#                                             'status': 'active'},
#                         'timeseries_ety2': None,
#                         'timeseries_ety3': None,
#                         'timeseries_ety4': None}]
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
    print(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_bucket_drivers: %s\n" % e)
    
