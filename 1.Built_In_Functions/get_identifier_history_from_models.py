#######################################################################################################################################
# 
# get_identifier_history_from_models(models, identifier_type) is a QI API function to retrieve all historic identifiers for a list of assets.  
# 
# Inputs:
#               * models - list of asset names
#               * identifier_type - SEDOL, ISIN, BloombergTicker or MSID.
#
# Output: History of all identifiers for those assets and the specified identifier type.
#               * e.g.
#                       {'resolved_models': {
#                            'HARP': [{'identifier': 'BJ4LDP7',
#                                      'effective_date': None,
#                                      'end_date': '2023-09-05'},
#                                     {'identifier': 'BMTYY04',
#                                      'effective_date': '2023-09-05',
#                                      'end_date': None}],
#                            'AAPL': [{'identifier': '2046251',
#                                      'effective_date': None,
#                                      'end_date': None}],
#                            'META': [{'identifier': 'B7TL820',
#                                      'effective_date': None,
#                                      'end_date': None}]},
#                        'unresolved_models': []}
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

# Names of the models to retrieve
# Datatype: str
models = ['AAPL', 'META', 'HARP']

# Identifier type to request for
# Datatype: str
identifier_type = 'SEDOL'

try:
    # Get a model definition
    api_instance.get_identifier_history_from_models(
        {
            'models': models,
            'identifier_type': identifier_type
        }
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_model: %s\n" % e)
