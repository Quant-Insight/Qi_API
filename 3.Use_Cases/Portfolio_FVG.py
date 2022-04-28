from __future__ import print_function 
import time
import qi_client
from qi_client.rest import ApiException
from pprint import pprint
import pandas
from datetime import datetime, timedelta

configuration = qi_client.Configuration() 

configuration.api_key['X-API-KEY'] = 'YOUR-API-KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed # configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# create an instance of the API class
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))

# Import your portfolio
df = pandas.read_csv('name-of-file')

date = '2022-04-27'
term = 'long term'
results = []

for model, notional in zip(df['Name'], df['Notional Value']):
    data = api_instance.get_model_timeseries(model=model, date_from=date, date_to=date, term=term)
    fvg = data[0].sigma
    rsq = data[0].rsquare
    percentage_gap = data[0].percentage_gap
    nv_gap = notional * (percentage_gap / 100)
    
    result = {
        'Name': model,
        'Notional Value': notional,
        'RSq': rsq,
        'FVG': fvg,
        'Percentage Gap': percentage_gap,
        'Notional Value Gap': nv_gap
    }
    
    results.append(result)
    
df_results = pandas.DataFrame(results)
portfolio_fvg = df_results['Notional Value Gap'].sum()
