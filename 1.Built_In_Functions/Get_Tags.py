    
#######################################################################################################################################
# 
# get_tags() is a QI API function to retrieve all the tags available. 
# 
# Inputs:
#
#
# Output: All the information of the requested model.
#               * e.g.
#                      [{'label': 'Euro Stoxx 600'},
#                       {'label': 'S&P 500'},
#                       {'label': ...},
#                       {'label': ...},
#                       {'label': ...},
#                       ...
#                     ]
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
    # Get list of all defined tags on the system
    api_response = api_instance.get_tags()
    pprint(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_tags: %s\n" % e)
