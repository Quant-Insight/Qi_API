#######################################################################################################################################
# 
# This function returns the portfolio exposures for a given portfolio and a given date. 
# 
#######################################################################################################################################

''' 

The portfolio has to be in the following format:

portfolio = pandas.DataFrame({'Name':[stock a, stock b, stock c],
                              'Position':[100, -100, 100]})
                              
stock a, b and c must be names of models in the Qi API, e.g. AAPL, MSFT, FB


This can be done by manually inputting the data (as seen above), or by importing an Excel file, or csv file like so:

xl = pandas.ExcelFile('file_location/file_name')
portfolio = xl.parse('Sheet_name')

OR

portfolio = pandas.read_csv('file_location/file_name')


The three inputs that need updating here are: file_location, file_name and Sheet_name

The Excel/csv file must be in the following format:

       | Name | Position |
       | AAPL |   100    |
       | MSFT |  -100    |
       | FB   |   100    |

'''

def get_portfolio_cash_exposures_bucket(portfolio,date):

    stock_names = portfolio['Name']
    df_tot = pandas.DataFrame()

    for stock in stock_names:

        sensitivity = api_instance.get_model_sensitivities(model=stock,date_from=date,date_to=date,term='Long Term')
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
            
            
    portfolio_sensitivities = pandas.DataFrame({},columns = df_tot.columns)
    
    for stock in stock_names:

        portfolio_sensitivities.loc[stock] = [a*float(portfolio[portfolio['Name']==stock]['Position'])/100 for a in df_tot.loc[stock]]

    portfolio_sensitivities.loc['Total'] = [portfolio_sensitivities[x].sum() for x in portfolio_sensitivities.columns]
    
    portfolio_exposures = portfolio_sensitivities.loc[['Total']]
    
    return portfolio_sensitivities
