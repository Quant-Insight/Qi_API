#######################################################################################################################################
# 
# This function creates a portfolio of European stocks based on sensitivities to a given factor. 
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         factor - 'factor' (e.g. 'ADXY')
#         size - number of stocks to be in resulting portfolio (e.g. 10)
#         date - 'date' (e.g. '2019-05-17')
#         term - 'term' (e.g. 'Long Term')
#
# Output: 
#         dataframe with the following columns:
#               * Position - dataframe index. 
#               * Name - top 5 factor drivers' names. 
#               * Weight - weights of the top 5 factor drivers.
#               * Factor Sensitivity - Factor top 5 drivers' sensitivity.
#               * e.g.
#                       Name | Weight   | ADXY Sensitivity
#                  2	LAND | 0.203390 | 0.09368
#                  1	KGH  | 0.237288 | 0.07690
#                  0	GPOR | 0.203390 | 0.05345
#                  3	TIT  | 0.355932 | 0.04598
#
#######################################################################################################################################

def get_portfolio(factor,size,date,term):

    FACTOR_sensitivity = []
    names = []
    POSITION = []

    # Get ID's of the Euro Stoxx 600 Stocks.
    # Stocks can be changed by specifying another stock's tag. 
    euro_stoxx_600 = [x.name for x in api_instance.get_models(tags="STOXX Europe 600")][::2]

    for asset in euro_stoxx_600:

        sensitivity = api_instance.get_model_sensitivities(model=asset,date_from=date,date_to=date,term = term)

        df_sensitivities = pandas.DataFrame()

        if len(sensitivity) > 0:
            date = [x for x in sensitivity][0]

            for data in sensitivity[date]:
                df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]
            # We want the top 5 drivers in absolute terms. 
            top5 = abs(df_sensitivities).T.nlargest(5,0)
            Factor_sens = float(df_sensitivities[factor])

            if factor in top5.index:
                FACTOR_sensitivity.append(Factor_sens)
                names.append(asset)
                position = top5.index.tolist().index(factor)+1
                POSITION.append(position)

    df_factor_sensit = pandas.DataFrame({'Name':names,'Position':POSITION,factor+' Sensitivity':FACTOR_sensitivity})
    portfolio = df_factor_sensit.nlargest(size,str(factor)+' Sensitivity')

    sw = 1/(portfolio['Position']+2)
    Weights = sw/sw.sum()

    portfolio = portfolio.drop(['Position'], axis=1)
    portfolio.insert(1,'Weight',Weights)
    
    return portfolio
