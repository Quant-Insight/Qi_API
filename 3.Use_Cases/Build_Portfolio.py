#######################################################################################################################################
# 
# This function creates a portfolio of European stocks based on sensitivities to a given factor. 
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         factor - 'factor' (e.g. 'USDCNH')
#         universe - universe of stocks to choose from (e.g. ['BMW','VIE','ATL'])
#         size - number of stocks to be in resulting portfolio (e.g. 10)
#         date - 'date' (e.g. '2019-05-17')
#         term - 'term' (e.g. 'Long Term')
#
# Output: 
#         dataframe with the following columns:
#               * Position - dataframe index. 
#               * Name - asset model name. 
#               * Weight - weight of each position in the portfolio.
#               * Factor Sensitivity - % move in asset for a 1 std move higher in the factor.
#               * e.g.
#
#                |     | Name   | Weight   | USDCNH Sensitivity |
#                |-----|:------:|:--------:|:------------------:| 
#                | 163 | WG/    | 0.077720 | 2.63019            |
#                | 145 | SWEDA  | 0.077720 | 2.47043            |
#                | 53  | ETL    | 0.108808 | 2.33411            |
#                | 123 | SAABB  | 0.136010 | 2.12093            |
#                | 35  | CNA    | 0.108808 | 1.80070            |
#                | 126 | SCHA   | 0.136010 | 1.55903            |  
#                | 10  | ANDR   | 0.077720 | 1.53357            |
#                | 30  | CABK   | 0.090674 | 1.49853            |  
#                | 66  | HAS    | 0.077720 | 1.41999            |
#                | 137 | SPM    | 0.108808 | 1.32387            |
#
#######################################################################################################################################


def get_portfolio(factor,universe,size,date,term):

    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:
        
        FACTOR_sensitivity = []
        names = []
        POSITION = []

        for asset in universe:

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
