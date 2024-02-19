    
#######################################################################################################################################
# 
# The following code allows you to pull data to an Excel file. 
#
# Requirements:
#         import pandas
#         import re
#
#######################################################################################################################################
#
#######################################################################################################################################
# Functions
#######################################################################################################################################

def get_sensitivity_grid(model,start,end,term):
    
    
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
    
    
    df_sensitivities = pandas.DataFrame()
    sensitivity_grid = pandas.DataFrame()
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:
            df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = pandas.concat([sensitivity_grid, df_sensitivities], axis = 0, join = 'outer')

            
    return sensitivity_grid
    
    
def get_model_data(model,start,end,term):
    
    
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

    
        time_series += api_instance.get_model_timeseries(model=model,date_from=date_from,date_to=date_to,term=term)
    
    FVG = [data.sigma for data in time_series]
    Rsq = [data.rsquare for data in time_series]
    dates = [data._date for data in time_series]
    
    model_value = [data.fair_value for data in time_series]
    percentage_gap = [data.percentage_gap for data in time_series]
    absolute_gap = [data.absolute_gap for data in time_series]

    df_ = pandas.DataFrame({'FVG':FVG, 'Rsq':Rsq, 'Model Value':model_value, 'Percentage Gap':percentage_gap,
                            'Absolute Gap':absolute_gap})
    df_.index = dates
    
    return df_

def remove_special_characters(input_string):
    # Define a regular expression pattern to match special characters
    pattern = r'[^a-zA-Z0-9\s]'  # Matches any character that is not a letter, number, or space

    # Use re.sub to replace special characters with blank spaces
    cleaned_string = re.sub(pattern, '_', input_string)

    return cleaned_string

# Function to process the paginated responses
def process_response(response):
    models = response['items']
    last_evaluated_key = response.get('last_evaluated_key', None)
    return models, last_evaluated_key
        
#######################################################################################################################################
# Main code
#######################################################################################################################################

# Define your stocks here.  
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

    stocks = [x['name'] for x in models]

# Change the address where the file will be saved and the name of the Excel file. 
writer = pandas.ExcelWriter('YOUR-PATH/example_excel.xlsx', engine='openpyxl')

# Chose start and end date
start = '2009-01-01'
end = '2023-10-10'
term = 'Long Term'

df_final = pandas.DataFrame()

for stock in stocks:
    model_data = get_model_data(stock,start,end,'Long Term')
    sens_data = get_sensitivity_grid(stock,start,end,'Long Term')

    model_data.index = model_data.index.strftime('%Y-%m-%d')

    df_aux = pandas.concat([model_data,sens_data], axis = 1)
    df_aux.insert(0, 'Model', [stock]*len(df_aux))
    df_final = pandas.concat([df_final, df_aux])

df_final.to_excel(writer)
    
writer.close()

print(stocks.index(stock))
