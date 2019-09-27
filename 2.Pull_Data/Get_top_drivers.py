#######################################################################################################################################
# 
# This function creates a table with the n top factors of a given model. 
#
# Requirements:
#         import pandas
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
#                                                | AAPL     | 
#                      | US 2y Infl. Expec.      | 2.02430  | 
#                      | Brent                   | 0.13150  | 
#                      | US 5y Infl. Expec.      | 1.91968  | 
#                      | US 10y Infl. Expec.     | 1.87902  |
#                      | US 5s30s Swap           | -1.52207 |
#                      | Equity 1y Fwd Earnings  | 1.37810  |
#                      | USD 10y Real Rate       | 1.23497  |
#                      | USDCNH                  | 1.05474  | 
#                      | JPY 10y Real Rate       | 0.91887  | 
#                      | Italian Sov. Confidence | -0.77165 |
#
#
#######################################################################################################################################

def get_top_drivers(model,number,date,term):
    
    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:

        sensitivity = api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)
        date = [x for x in sensitivity][0]
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:
            df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

        top_names = abs(df_sensitivities.T).nlargest(number,0).index
        top = df_sensitivities[top_names]
        top = top.T.rename(columns={0:model})

        return top
