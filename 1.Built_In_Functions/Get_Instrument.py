#######################################################################################################################################
# 
# get_instrument(instrument, mnemonic=mnemonic, numeric_id=numeric_id)) is a QI API function to retrieve the information of a given 
# instrument.  
# 
# Inputs:
#               * instrument - numeric id or name of the instrument (e.g. 'ITRXAJE CBGT Index')
#               * mnemonic (optional) - Where a string is provided as an instrument, this is the associated field name (e.g. PX_LAST). 
#                 PX_LAST is the default value. 
#               * numeric_id (optional) - True to consider driver as a numeric id. False to consider driver as a name (False by default).
#
# Output: All the information of the requested instrument.
#               * e.g.
#                      {'coverage': 'COMPLETE',
#                       'id': 23166,
#                       'mnemonic': 'PX_LAST',
#                       'ticker': 'ITRXAJE CBGT Index'}
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
instrument = 'ITRXAJE CBGT Index'

# Where a string is provided as an instrument, this is the associated field name (e.g. PX_LAST) (optional) (default to PX_LAST)
# Datatype: str
mnemonic = 'PX_LAST'

# If set to true, will consider identifier as a numeric ID - not as a name.(optional) (default to false)
# Datatype: bool
numeric_id = False

try:
    # Get instrument definition
    api_response = api_instance.get_instrument(instrument, mnemonic=mnemonic, numeric_id=numeric_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_instrument: %s\n" % e)

