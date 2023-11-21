from __future__ import print_function
import time
import qi_client
from qi_client.rest import ApiException
from pprint import pprint
import pandas

# Configure API key authorization: QI API Key
configuration = qi_client.Configuration()

# Add the API Key provided by QI
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'

# create an instance of the API class
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))


# Function to create a dataframe for the sensitivity data
def get_sensitivity_df(model, start, end, term):

    year_start = int(start[:4])
    year_end = int(end[:4])
    sensitivity = {}
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

        sensitivity.update(
        api_instance.get_model_sensitivities(model=model,date_from=date_from,date_to=date_to,term=term))

    results = []
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        sensitivities_entry = {}

        for data in sensitivity[date]:
            sensitivities_entry[str(data['driver_short_name'])] = data['sensitivity']

        results.append(sensitivities_entry)

    return pandas.DataFrame(results, index=dates)


def insert_point_in_time_identifier_column(df, model, identifier_type):
    
    model_identifiers = api_instance.get_identifier_history_from_models(
        {
            'models': [model],
            'identifier_type': identifier_type
        })
    model_identifiers = model_identifiers['resolved_models'][model]

    default_start_date = min(df.index.tolist())
    default_end_date = '3000-01-01'
    identifier_col = []
    for date in df.index:
        for identifier_entry in model_identifiers:
            start_date = identifier_entry.get('effective_date')
            start_date = start_date if start_date else default_start_date
            end_date = identifier_entry.get('end_date')
            end_date = end_date if end_date else default_end_date

            if date >= start_date and date < end_date:
                identifier_col.append(identifier_entry['identifier'])

    df.insert(0, identifier_type, sedol_col)
    
    return df


model = 'META'
identifier_type = 'BloombergTicker'
sens_df = get_sensitivity_df(model, '2009-01-01', '2023-11-15', 'long term')

sens_df = insert_point_in_time_identifier_column(sens_df, model, identifier_type)
