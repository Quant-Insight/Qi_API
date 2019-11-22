#######################################################################################################################################
# 
# This function creates a table containing a specific model's factors and what a 1 standard deviation move is in each one of those factors.
#
# Requirements:
#         import pandas
#
# Inputs: 
#         model (e.g. 'AAPL')
#         date (e.g. '2019-01-02')
#
# Output: 
#         dataframe with the following columns:
#               * Factors - dataframe index. 
#               * 1 Std - 1 standard deviaiton move in factor units. 
#
#                               | 1std     | 
#                 US 5s30s Swap | 0.06654  | 
#                 Itraxx Xover  | 21.04296 |
#                 VIX           | 2.37888  | 
#                 China GDP     | 0.36891  |
#                 ...           | ...      | 
#
#######################################################################################################################################


def get_factor_stdevs(model,date):

    term = 'Long Term'

    sensitivity = api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)
    date = [x for x in sensitivity][0]
    df_sensitivities = pandas.DataFrame()

    for data in sensitivity[date]:
        value = data['driver_zscore_window_stdev']
        df_sensitivities[str(data['driver_short_name'])]=[value]

    df_sensitivities = df_sensitivities.transpose()
    df_sensitivities.rename(columns={0:'1 Std'}, inplace=True)
            

    return df_sensitivities
