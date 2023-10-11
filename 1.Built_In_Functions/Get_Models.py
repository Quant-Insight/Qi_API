    
#######################################################################################################################################
# 
# get_models(tags = tags, asset_classes = asset_classes) is a QI API function to retrieve the all the models available, having the 
# option to  filter by tags and by asset classes. 
# 
# Inputs:
#               * tags (optional) - comma delimited list of tags to filter results with (e.g. 'S&P 1500') 
#               * asset_class (optional) - comma delimited list of asset classes to filter results with. Results must contain all asset
#                                          classes specified (e.g. 'Equity'). 
#
# Output: A list with all the models filtered by tags (optional) and asset classes (optional).
#               * e.g.
#                      [{'group': 'qi_admin',
#                         'id': 1,
#                         'model_parameter': 'short term',
#                         'name': 'A',
#                         'security_name': 'Agilent Technologies [US00846U1016 | A UN Equity | 126.1.A '
#                                          '| 2520153]',
#                         'status': 'ACTIVE',
#                         'type': None},
#                        ...
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

# Comma delimited list of tags to filter results with. Results must contain *all*tags specified. (optional)
# Datatype: str
tags = 'S&P 500'

asset_classes = 'Equity'

try:
    # Get list of all defined models on the system
    api_response = api_instance.get_models(tags=tags, asset_classes=asset_classes)
    pprint(api_response)
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_models: %s\n" % e)

