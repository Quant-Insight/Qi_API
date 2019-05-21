#######################################################################################################################################
# 
# This function creates a table with the n top factors of a given model. 
# 
# Inputs: 
#         model - 'model' (e.g. 'AAPL')
#         number - number of drivers we want to show in the table (e.g. 10)
#         date - 'date' (e.g. '2019-05-17')
#         term - 'term' (e.g. 'Long Term')
#
# Output: 
#         dataframe with the following columns:
#               * Factors' names - dataframe index. 
#               * Model sensitivities per factor
#               * e.g.
#                                               AAPL
#                       2y Infl. Expec.	        0.13866
#                       5y Infl. Expec.         0.13150
#                       10y Infl. Expec.	    0.12872
#                       USD 10y Real Rate	    0.11439
#                       Equity 1y Fwd Earnings	0.10622
#                       WTI	                    0.10467
#                       Country 5s30s Swap      -0.10147
#                       Brent	                0.09379
#                       JPY 10y Real Rate       0.08489
#                       EUR 1y Basis Swap       -0.07571
#
#######################################################################################################################################


def get_top_drivers(model,number,date,term):

    sensitivity = api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)
    date = [x for x in sensitivity][0]
    df_sensitivities = pandas.DataFrame()
 
    for data in sensitivity[date]:
        df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

    top_names = abs(df_sensitivities.T).nlargest(number,0).index
    top = df_sensitivities[top_names]
    top = top.T.rename(columns={0:model})
    
    return top
