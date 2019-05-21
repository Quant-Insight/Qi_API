#######################################################################################################################################
# 
# This function creates a table with the FVG, Rsq, Model Value, Percentage Gap, Absolute Gap and Spot Price of a given model. Note that
# we have data from Monday to Friday. 
# 
# Inputs: 
#         model - model (e.g. 'AAPL')
#         start - starting date (e.g. '2009-01-01')
#         end - ending date (e.g. '2019-05-20')
#         term - term (e.g. 'Long Term')
#
# Output: 
#         dataframe with the following columns:
#               * Dates - dataframe index. 
#               * FVG - model FVG values for each day requested. 
#               * Rsq - model Rsq values for each day requested.
#               * Model Value - model fair value for each day requested.
#               * Percentage Gap - model percentage gap value for each day requested. 
#               * Alsolute Gap - model absolute gap value for each day requested. 
#               * Spot Price- model spot price for each day requested (spot price = z-score * stdev + mean)
#               * e.g.
#
#                            | FVG      | Rsq      | Model Value | Percentage Gap | Absolute Gap
#                 2015-05-20 | -0.40749 | 32.54643 | 134.51795   | -3.42761       | -4.45795
#                 2015-05-21 | -0.30985 | 31.95673 | 134.77879   | -2.57918       | -3.38879
#                 2015-05-22 | -0.22439 | 31.19517 | 134.99570   | -1.85280       | -2.45570    
#
#######################################################################################################################################


def get_model_data(model, start, end, term):
    # Note that the periods of time can be longer than a year. We need to divide them in one-year periods.   
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
    spot_price = [data.target_zscore*data.target_stdev + data.target_mean for data in time_series]


    df_ = pandas.DataFrame({'FVG':FVG, 'Rsq':Rsq, 'Model Value':model_value, 'Percentage Gap':percentage_gap,
                            'Absolute Gap':absolute_gap, 'Spot Price': spot_price})
    
    df_.index = dates
    
    return df_
