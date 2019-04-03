#######################################################################################################################################
# 
# This function creates a portfolio given a factor, size, funds and a specific date, for Euro Stoxx 600 Stocks. 
# Stocks can be changed by specifying their associated tag. 
# 
#######################################################################################################################################

def get_portfolio(factor,size,funds,date):

    FACTOR_sensitivity = []
    names = []
    POSITION = []

    # Get ID's of the Euro Stoxx 600 Stocks.
    # Stocks can be changed by specifying another stock's tag. 
    euro_stoxx_600 = [x.name for x in api_instance.get_models(tags="STOXX Europe 600")][::2]

    for i in euro_stoxx_600:

        sensitivity = api_instance.get_model_sensitivities(model=i,date_from=date,date_to=date,term = 'Long Term')

        df_sensitivities = pandas.DataFrame()

        if len(sensitivity) > 0:
            date = [x for x in sensitivity][0]

            for data in sensitivity[date]:
                df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

            top10 = df_sensitivities.transpose().nlargest(10,0)
            Factor_sens = float(df_sensitivities[factor])

            if factor in top10.index and Factor_sens > 0:
                FACTOR_sensitivity.append(Factor_sens)
                names.append(api_instance.get_model(model=i).name)
                position = top10.index.tolist().index(factor)+1
                POSITION.append(position)

    portfolio_size = size

    df_factor_sensit = pandas.DataFrame({'Name':names,'Position':POSITION,factor+' Sensitivity':FACTOR_sensitivity})
    portfolio = df_factor_sensit.nlargest(portfolio_size,str(factor)+' Sensitivity')

    sw = 1/(portfolio['Position']+2)
    summ = sum(sw)
    Weights = sw/summ
    position_values = [funds*x for x in Weights]
    factor_exposure = [a*b/100 for a,b in zip(portfolio[factor+' Sensitivity'],position_values)]

    portfolio = portfolio.drop(['Position'], axis=1)
    portfolio.insert(1,'Weight',Weights)
    portfolio.insert(2,'Position Value',position_values)
    portfolio[factor+' Exposure'] = factor_exposure
    
    return portfolio
