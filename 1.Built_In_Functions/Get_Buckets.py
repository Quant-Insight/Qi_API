#######################################################################################################################################
# 
# get_buckets() is a QI API function to retrieve all the available buckets with their id's.  
# 
# Inputs
#
# Output: A list with the id and the name of all the buckets in our API.
#               * e.g.
#                      [{'id': 23, 'name': 'Corporate Credit'},
#                       {'id': 24, 'name': 'Country Growth'},
#                       ... 
#                       ]
#
#######################################################################################################################################


from __future__ import print_function
import time
import os
import qi_client
from qi_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: QI API Key
configuration = qi_client.Configuration()

# Your API key is read from the QI_API_KEY environment variable (see the README)
configuration.api_key['X-API-KEY'] = os.environ['QI_API_KEY']

# Uncomment to set up a proxy
# configuration.proxy = 'http://localhost:3128'
# create an instance of the API class

api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))

try:
    # Get all available buckets
    api_response = api_instance.get_buckets()
    pprint(api_response)
  
except ApiException as e:
    print("Exception when calling DefaultApi->get_buckets: %s\n" % e)
