#######################################################################################################################################
# 
# This function creates a table with the FVG values of a given model within a given period of time. Note that we have data from Monday 
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
#               * FVG - model FVG values for each day requested. 
#               * e.g.
#
#                            | FVG      |
#                |2009-01-01 | -0.44924 | 
#                |2009-01-02 | -0.31899 |
#                |2009-01-05 | -0.23623 | 
#                |...        | ...      |
#######################################################################################################################################


def get_FVG(model, start, end, term):
    
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
        dates = [data._date for data in time_series]

        df_ = pandas.DataFrame({'FVG':FVG})

        df_.index = dates

        return df_
