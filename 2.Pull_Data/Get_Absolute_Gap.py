    
#######################################################################################################################################
# 
# This function creates a table with the Absolute Gap values of a given model within a given period of time. Note that we have data from Monday 
# to Friday. 
#
# Requirements:
#         import pandas
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
#               * Absolute Gap - model Absolute Gap values for each day requested. 
#               * e.g.
#
#                            | Absolute Gap |
#                |2009-01-01 | -2.52591     | 
#                |2009-01-02 | -1.88494     |
#                |2009-01-05 | -1.52342     |  
#                |...        | ...          |
#######################################################################################################################################


def get_model_data(model, start, end, term):
    
    #Note that we only have data from Monday to Friday.
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')    
    
    if (start_date.weekday() == 5 or start_date.weekday() == 6) and (end_date.weekday() == 5 or end_date.weekday() == 6) and ((end_date - start_date).days == 1):
        print('Please choose a period of time which includes days between Monday and Friday.')
    else: 
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


        df_ = pandas.DataFrame({'FVG':FVG, 'Rsq':Rsq, 'Model Value':model_value, 'Percentage Gap':percentage_gap,
                                'Absolute Gap':absolute_gap})

        df_.index = dates

        return df_
