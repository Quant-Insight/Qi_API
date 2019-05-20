#######################################################################################################################################
# 
# This function creates a table with the sensitivities values of an specific model within a period of time.  
# 
# Inputs: 
#         model - model (e.g. 'AAPL')
#         start - starting date (e.g. '2016-05-17')
#         end - ending date (e.g. '2019-05-17')
#         term - term (e.g. 'Long Term')
#
#######################################################################################################################################


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
