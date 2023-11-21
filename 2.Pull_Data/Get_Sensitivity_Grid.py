#######################################################################################################################################
# 
# This function creates a table with the sensitivities of a given model on a factor level, for a given period of time. Note that we have
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
#               * A column per Factor with its sensitivities per day. 
#               * e.g.
#    
#
#                  | Brent [CO1 A:00_0_N Comdty] | China 5y CDS [CCHIN1U5 CBGT Curncy] | China GDP [Now_China] | Copper [HG1 A:00_0_N Comdty] | ... | 
#       2015-01-01 | -0.26924                    | -0.26444                            | 0.31652               | 0.16956                      | ... |  
#       2015-01-02 | -0.27617                    | -0.27528                            | 0.32443               | 0.15854                      | ... |  
#       2015-01-05 | -0.28721                    | -0.29178                            | 0.33853               | 0.15243                      | ... |  
#       ...        | ...                         | ...                                 | ...                   | ...                          | ... |       
#
#######################################################################################################################################

def get_sensitivity_grid(model,start,end,term):
    
    #Note that we only have data from Monday to Friday.
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

            sensitivity.update(
            api_instance.get_model_sensitivities(
            model,
            date_from=date_from,
            date_to=date_to,
            term=term
            )
            )


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
                sensitivity_grid = pandas.concat([sensitivity_grid, df_sensitivities])


        return sensitivity_grid
    
