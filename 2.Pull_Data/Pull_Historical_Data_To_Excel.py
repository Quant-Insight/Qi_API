    
#######################################################################################################################################
# 
# The following code allows you to pull data to an excel file. 
#
# Requirements:
#         import pandas
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
            sensitivity_grid = sensitivity_grid.append(df_sensitivities)

            
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
        
#######################################################################################################################################
# Main code
#######################################################################################################################################

# Define your stocks here.  
sp1500_names =  [x.name for x in api_instance.get_models(tags="S&P 1500")][::2]
stocks = sp1500_names

# Change the address where the file will be saved and the name of the Excel file. 
writer = pandas.ExcelWriter('C:/Users/EXAMPLE_ADDRESS.xlsx', engine='openpyxl')

# Chose start and end date
start = '2015-01-01'
end = '2020-04-01'

for stock in stocks:
    model_data = get_model_data(stock,start,end,'Long Term')
    sens_data = get_sensitivity_grid(stock,start,end,'Long Term')

    model_data.index = [str(x).split(' ')[0] for x in model_data.index]

    df_final = pandas.concat([model_data,sens_data], axis=1, join = 'inner')

    df_final.to_excel(writer, sheet_name = stock)
    writer.save()
    
    print(stocks.index(stock))
