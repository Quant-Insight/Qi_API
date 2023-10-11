#######################################################################################################################################
# 
# This function creates a table with the FVG, Rsq, Model Value, Percentage Gap, Absolute Gap of a given model. Note that
# we have data from Monday to Friday. 
#
# Requirements:
#         import pandas
#
# Inputs: 
#         model - model (e.g. 'AAPL')
#         start - starting date (e.g. '2015-01-01')
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
#               * Absolute Gap - model absolute gap value for each day requested. 
#               * e.g.
#
#                            | FVG      | Rsq      | Model Value | Percentage Gap | Absolute Gap
#                 2015-01-01 | 0.17090  | 59.10984 | 108.42994   | 1.76668        | 1.95006
#                 2015-01-02 | 0.04313  | 59.35062 | 108.84058   | 0.44765        | 0.48942
#                 2015-01-05 | -0.21549 | 59.76303 | 108.67810   | -2.28527       | -2.42810   
#                 ...        | ...      | ...      | ...         | ...            | ...
#
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
        df_.index = df_.index.strftime('%Y-%m-%d')

        return df_
