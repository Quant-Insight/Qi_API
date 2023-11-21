#######################################################################################################################################
# 
# get_models_from_identifiers(models, term, version, numeric_id) is a QI API function to retrieve the information of a given model.  
# 
# Inputs:
#               * identifiers - list of identifiers with the same identifier type (SEDOLs, ISINs, BBG Tickers or MS IDs). 
#               * target_date - Date the requested identifiers existed on (point-in-time), e.g. '2022-01-03'.
#
# Output: Dictionary of the models/assets found for the requested identifiers on the specified date..
#               * e.g.
#                       {'resolved_models': {'AAPL US Equity': 'AAPL', 'FB US Equity': 'META'},
#                        'unresolved_identifiers': []}
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

# List of identifiers you want to search for
# Datatype: str
identifiers = ['AAPL US Equity', 'FB US Equity']

# Date the requested identifiers existed on
# Datatype: str
target_date = '2022-01-03'

try:
    # Get a model definition
    api_response = api_instance.get_models_from_identifiers(
        {
            'identifiers': identifiers,
            'target_date': target_date
        }
    )
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_model: %s\n" % e)
