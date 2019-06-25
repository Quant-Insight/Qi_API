#######################################################################################################################################
# 
# This function creates a table with the Rsq values of a given model, for a given period of time. Note that we have data from Monday to 
# Friday. 
# 
# Requirements:
#         import pandas
#
# Inputs: 
#         model - model (e.g. 'AAPL')
#         start - starting date (e.g. '2018-05-21')
#         end - ending date (e.g. '2019-05-20')
#         term - term (e.g. 'Long Term')
#
# Output: 
#         dataframe with the following columns:
#               * Dates - dataframe index. 
#               * Rsq - model Rsq values sorted by date. 
#               * e.g.
#                                Rsq
#                    Dates                 
#                    2018-05-21	| 34.93530
#                    2018-05-22	| 34.85189
#                    2018-05-23	| 34.75355  
#                    ...        | ...
#
#######################################################################################################################################


def get_Rsq(model, start, end, term):
    
    #Note that we only have data from Monday to Friday.
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')    
    
    if (start_date.weekday() == 5 or start_date.weekday() == 6) and (end_date.weekday() == 5 or end_date.weekday() == 6) and ((end_date - start_date).days == 1):
        print('Please choose a period of time which includes days between Monday and Friday.')
    else: 
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
