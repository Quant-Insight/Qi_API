#######################################################################################################################################
# 
# This piece of code retrieves the historical R-Squared Data for a given model (SPX) and a given period of time (from 2015-01-01 until 
# 2019-01-10). 
#
# Requirements: 
#         * Install matplotlib and pandas:
#                 * Jupyter Notebooks:
#                           !pip install matplotlib pandas
#
#                 * Command line:
#                           $ pip install matplotlib pandas
#
# Inputs: For the purpose of this example, the model and the period of time are already defined in example_historial_rsq() function.
#               
# Output: A line chart representing the historical R-Squared values for SPX, between 2015-01-01 and 2019-01-10.
#               
#
#######################################################################################################################################


import qi_client
import pandas
from datetime import datetime

# Configure API key authorization: QI API Key
configuration = qi_client.Configuration()

# Add the API Key provided by QI
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'

# Uncomment to set up a proxy
# configuration.proxy = 'http://localhost:3128'

# create an instance of the API class
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))

#######################################################################################################################################
#                                                              Functions
#######################################################################################################################################

# This function will retrieve the historical RSq data for a given model and a given period of time. 
#
def get_rsq(model, start, end, term):
    
    # Note that this may be more than 1 year of data, so need to split requests
    year_start = int(start[:4])
    year_end = int(end[:4])
    time_series = []
    
    for year in range(year_start, year_end + 1):
        query_start = start
        
        if year != year_start:
            date_from = '%d-01-01' % year
        else:
            date_from = start
            
        if year != year_end:
            date_to = '%d-12-31' % year
        else:
            date_to = end
            
        print("Gathering data for %s from %s to %s..." % (model,
                                                          date_from,
                                                          date_to))
        time_series += api_instance.get_model_timeseries(
            model,
            date_from=date_from,
            date_to=date_to,
            term=term)
        
    rsq = [data.rsquare for data in time_series]
    dates = [data._date for data in time_series]
    
    df = pandas.DataFrame({'Dates': dates, 'Rsq': rsq})
    df.set_index('Dates', inplace=True)

    return df
    
# This function will call get_rsq()   
def example_historical_rsq():
    
    import matplotlib.pyplot as plt
    
    # To retrieve the historical RSq data of any other model or period of time, change the inputs of get_rsq() function. 
    df = get_rsq('SPX',
                 '2015-01-01',
                 '2019-01-10',
                 'Long Term')
    
    fig = plt.figure(figsize=(18, 6))
    
    ax = plt.subplot(111)
    fig.patch.set_facecolor('#FFFFFF')
    
    plt.plot(df.index.values, df['Rsq'], color='#53B2FF')
    
#######################################################################################################################################
#                                                           Main Code
#######################################################################################################################################

example_historical_rsq()

    
