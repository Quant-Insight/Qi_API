#######################################################################################################################################
# 
# This function returns the portfolio exposures for a given portfolio and a given date. 
# 
#######################################################################################################################################

def get_portfolio_exposures_bucket(portfolio,date):

    stock_names = portfolio['Name']
    df_tot = pandas.DataFrame()

    for stock in stock_names:

        sensitivity = api_instance.get_model_sensitivities(model=stock,date_from=date,date_to=date)
        df_sensitivities = pandas.DataFrame()
        date = [x for x in sensitivity.keys()][0]

        for data in sensitivity[date]:

            if data['bucket_name'] in df_sensitivities.columns:
                df_sensitivities[str(data['bucket_name'])][0] = df_sensitivities[str(data['bucket_name'])][0] + [data['sensitivity']]

            else:
                df_sensitivities[str(data['bucket_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:stock})
        df_sensitivities = df_sensitivities.sort_index(axis=1)
        if df_tot.empty:
            df_tot = df_sensitivities
        else:
            df_tot = df_tot.append(df_sensitivities)

    SUMS = [sum(df_tot[x]) for x in df_tot.columns]
    sumss = pandas.DataFrame(SUMS).rename(columns={0:'Sum'})
    sumss = sumss.transpose()
    sumss.columns = df_tot.columns
    df_tot = df_tot.append(sumss)
    portfolio_sensitivities = df_tot[abs(df_tot).transpose().nlargest(15,'Sum').index].transpose()

    for stock in stock_names:

        portfolio_sensitivities[stock] = [a*float(portfolio.loc[portfolio['Name']==stock]['Position Value'])/100 for a in portfolio_sensitivities[stock]]

    portfolio_sensitivities = portfolio_sensitivities.drop(columns = 'Sum')

    ex_SUMS = [sum(portfolio_sensitivities.loc[x]) for x in portfolio_sensitivities.index]
    portfolio_sensitivities['TOTAL'] = ex_SUMS
    portfolio_exposures = portfolio_sensitivities.transpose()
    
    return portfolio_exposures
