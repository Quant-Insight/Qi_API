########################################################################################################################################################################################################################################################################
# 
# This function creates a table with the sensitivities values of a specific model within a period of time.  
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         model - model (e.g. 'AAPL')
#         start - starting date (e.g. '2016-05-17')
#         end - ending date (e.g. '2019-05-17')
#         term - term (e.g. 'Long Term')
#
# Output: 
#         dataframe with the following columns:
#               * Date - dataframe index. 
#               * A column by Bucket with its sensitivity associated to the model by date.  
#               * e.g.
#                    	Corp credit | Country Growth | DM FX   | EM FX   | EM Sov Risk | Energy  | Est. Earnings | 	Global Growth | Global QE | Global Real Rates | Infl. Expec. | Metals  | Peripheral EU Sov Risk | Risk Aversion | Systemic liquidity
#           2015-05-18| -0.07700    | 0.00094        | 0.00599 | 0.01637 | -0.02062    | 0.01144 | -0.00126      | -0.00007       | -0.00685  | -0.01369          | 0.03434      | 0.00850 | 0.03064                | -0.05779      | -0.01515
#           2015-05-19| -0.07763    | 0.00094        | 0.00669 | 0.01638 | -0.02066    | 0.01014 | -0.00129      | -0.00005       | -0.00621  | -0.01319          | 0.03265      | 0.00848 | 0.03089                | -0.05818      | -0.01558
#           2015-05-20| -0.07837    | 0.00087        | 0.00740 | 0.01636 | -0.02044    | 0.00882 | -0.00132      | -0.00005       | -0.00550  | -0.01266          | 0.03097      | 0.00833 | 0.03117                | -0.05843      | -0.01613
#           ...       | ...         | ...            | ...     | ...     | ...         | ...     | ...           | ...            | ...       | ...               | ...          | ...     | ...                    | ...           | ...             
#
########################################################################################################################################################################################################################################################################


def get_bucket_grid(model,start,end,term):
    
    sensitivity = api_instance.get_model_sensitivities(model=model,date_from=start,date_to=end,term=term)
    
    sensitivity_grid = pandas.DataFrame()
    
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:

            if data['bucket_name'] in df_sensitivities.columns:
                df_sensitivities[str(data['bucket_name'])][0] = df_sensitivities[str(data['bucket_name'])][0] + [data['sensitivity']]

            else:
                df_sensitivities[str(data['bucket_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = sensitivity_grid.append(df_sensitivities)

    return sensitivity_grid
