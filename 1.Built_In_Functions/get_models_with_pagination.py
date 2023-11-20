    
#######################################################################################################################################
# 
# get_models_with_pagination(tags = tags, asset_classes = asset_classes) is a QI API function to retrieve the all the models available using pagination, 
# having the option to filter by tags and by asset classes. 
# 
# Inputs:
#               * tags (optional) - comma delimited list of tags to filter results with (e.g. 'S&P 1500') 
#               * asset_class (optional) - comma delimited list of asset classes to filter results with. Results must contain all asset
#                                          classes specified (e.g. 'Equity').
#               * term (optional) - model term parameter, e.g. 'long term' or 'short term'
#               * include_delisted (optional) - boolean type paramater for including delisted models (True or False), default is False
#               * exclusive_start_key (optional) - start key for pagination (use last_evaluated_key from previous paginated response)
#               * count (optional) - number of models to return, default is 10,000
#
# Output: A list with all the models filtered by tags (optional) and asset classes (optional).
#               * e.g.
#                     {'items':[
#                      {'group': 'qi_admin',
#                         'id': 1,
#                         'model_parameter': 'short term',
#                         'name': 'A',
#                         'security_name': 'Agilent Technologies [US00846U1016 | A UN Equity | 126.1.A '
#                                          '| 2520153]',
#                         'status': 'ACTIVE'},
#                        ...
#                        ... ],
#                      'last_evaluated_key': 24821,
#                      'count': 10000}
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

# Function to process the paginated responses
def process_response(response):
    models = response['items']
    last_evaluated_key = response.get('last_evaluated_key', None)
    return models, last_evaluated_key

# Comma delimited list of tags to filter results with. Results must contain *all*tags specified. (optional)
# Datatype: str
tags = 'S&P 500'
asset_classes = 'Equity'
term = 'long term'

try:
    # Get list of all defined models on the system  
    response = api_instance.get_models_with_pagination(
        asset_classes=asset_classes,
        tags=tags,
        term=term,
        include_delisted=True
    )
    models, exclusive_start_key = process_response(response)

    while exclusive_start_key:
        
        response = api_instance.get_models_with_pagination(
            asset_classes=asset_classes,
            tags=tags,
            term=term,
            include_delisted=True,
            exclusive_start_key=exclusive_start_key
        )
        _models, exclusive_start_key = process_response(response)
        models += _models

    model_names = [x['name'] for x in models]
    
except ApiException as e:
    print("Exception when calling DefaultApi->get_models: %s\n" % e)
