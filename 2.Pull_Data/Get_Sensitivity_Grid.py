#######################################################################################################################################
# 
# This function creates a table with the sensitivities of a given model on a factor level, for a given period of time. Note that we have
# data from Monday to Friday. 
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
#               * A column per Factor with its sensitivities per day. 
#               * e.g.
#
#                     |	10y Infl. Expec.| 2y Infl. Expec.| 5y Infl. Expec.| ADXY     | Baltic Dry | Brent   | ...	
#           Dates     |                 |                |                |          |            |         | ...  
#           2009-01-01|	0.04744	        | 0.05013	 | 0.05206	  | -0.00458 | 0.03520	  | 0.04426 | ...  
#           2009-01-02|	0.04795	        | 0.05082	 | 0.05271	  | -0.00522 | 0.03593	  | 0.04423 | ...
#           ...       | ...             | ...            | ...            | ...      | ...        | ...     | ...         
#
#######################################################################################################################################

def get_sensitivity_grid(model,start,end,term):
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
            df_sensitivities[str(data['driver_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = sensitivity_grid.append(df_sensitivities)

            
    return sensitivity_grid
