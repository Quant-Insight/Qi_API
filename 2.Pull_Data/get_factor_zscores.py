#######################################################################################################################################
# 
# This function creates a table with factor z-scores from the factorset of a given model, over a given date range. Note that we have
# data from Monday to Friday. 
#
# Requirements:
#         import pandas
#         from datetime import datetime
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
#               * A column per Factor with its z-score per day. 
#               * e.g.
#    
#
#                  | Brent          | China 5y CDS   | China GDP    | Copper     | ...
#       2015-01-01 | -0.26924       | -0.26444       | 0.31652      | 0.16956    | ...
#       2015-01-02 | -0.27617       | -0.27528       | 0.32443      | 0.15854    | ...
#       2015-01-05 | -0.28721       | -0.29178       | 0.33853      | 0.15243    | ...
#       ...        | ...            | ...            | ...          | ...        | ...      
#
#######################################################################################################################################


def get_factor_zscores(model,start,end,term):

    # Note that we only have data from Monday to Friday.
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')    
    
    if (start_date.weekday() == 5 or start_date.weekday() == 6) and (end_date.weekday() == 5 or end_date.weekday() == 6) and ((end_date - start_date).days == 1):
        print('Please choose a period of time which includes days between Monday and Friday.')
        
    else: 
        # Note that the periods of time can be longer than a year. We need to divide them in one-year periods. 
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

    #         print("Gathering data for %s from %s to %s..." % (model,
    #         date_from,
    #         date_to))

            sensitivity.update(
            api_instance.get_model_sensitivities(model=model,date_from=date_from,date_to=date_to,term=term))


        df_zscore = pandas.DataFrame()
        zscore_grid = pandas.DataFrame()
        dates = [x for x in sensitivity.keys()]
        dates.sort()

        for date in dates:
            df_zscore = pandas.DataFrame()

            for data in sensitivity[date]:
                df_zscore[str(data['driver_short_name'])]=[data['driver_zscore']]

            df_zscore = df_zscore.rename(index={0:date})
            df_zscore = df_zscore.sort_index(axis=1)

            if zscore_grid.empty:
                zscore_grid = df_zscore
            else:
                zscore_grid = zscore_grid.append(df_zscore)


        return zscore_grid
