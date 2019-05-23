    
#######################################################################################################################################
# 
# get_buckets() is a QI API function to retrieve all the available buckets with their id's.  
# 
# Inputs:
#               * bucket - numeric id or name of the bucket (e.g. 'Corp credit')
#               * numeric_id (optional) - True to consider bucket as a numeric id. False to consider bucket as a name (False by default).
#
# Output: A list with the id and the name of all the buckets in our API.
#               * e.g.
#                      {'id': 23, 'name': 'Corp credit'}
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
# Numeric ID or name of the bucket to retrieve
# Datatype: str

bucket = 'Corp credit'

# If set to true, will consider identifier as a numeric ID - not as a name. (optional) (default to false)
# Datatype: bool

numeric_id = False
try:
    # Get bucket details
    api_response = api_instance.get_bucket(bucket, numeric_id=numeric_id)
    pprint(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_bucket: %s\n" % e)
