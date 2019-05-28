#######################################################################################################################################################################################################################################################
# 
# This function creates a table with the cash exposures of a given portfolio on a bucket level, for a given period of time for each 
# stock in the portfolio. It also provides the portfolio total cash exposures per bucket. 
#
# Requirements:
#         import pandas
#
# Inputs: 
#           * portfolio - model (e.g. 'AAPL')
#             
#             The portfolio has to be in the following format:
#
#               portfolio = pandas.DataFrame({'Name':[stock a, stock b, stock c],
#                              'Weight':[0.3, 0.3, 0.4],
#                              'L/S':[1,-1,1]})
#                              
#                              
#               stock a, b and c must be names of models in the Qi API, e.g. AAPL, MSFT, FB
#
#               This can be done by manually inputting the data (as seen above), or by importing an Excel file, or csv file like so:
#
#                   xl = pandas.ExcelFile('file_location/file_name')
#                   portfolio = xl.parse('Sheet_name')
#
#                OR
#
#                   portfolio = pandas.read_csv('file_location/file_name')
#
#               The three inputs that need updating here are: file_location, file_name and Sheet_name
#
#               The Excel/csv file must be in the following format:
#
#                   | Name | Position |
#                   | AAPL |   100    |
#                   | MSFT |  -100    |
#                   | FB   |   100    |

#           * date - portfolio date (e.g. '2019-05-20') 
#
# Output: 
#         dataframe with the following columns:
#               * Column with all the portfolio stock names plus the 'Total' row - dataframe index. 
#               * A column per Bucket with its chash sensitivities associated to each stock in the portfolio. 
#               * e.g.
#
#         Corp credit| Country Growth|	DM FX   |  EM FX     | EM Sov Risk | Energy    | Est. Earnings  | Global Growth | Global QE | Global Real Rates | Infl. Expec. | Metals     | Peripheral EU Sov Risk | Risk Aversion | Systemic liquidity
#   AAPL  | -0.22007 | -0.10161      | -0.00709 | -0.07398   | 0.03139     | 0.13319   | 0.10636        | 0.06445	      | 0.04143   | 0.26776	          | 0.39953      | -0.05851   | -0.14471               | -0.06184      | -0.13707
#   MSFT  | 0.12265  | 0.03603       | 0.00017  | 0.00674    | 0.02346     | -0.07581  | -0.00171       | -0.01244      | 0.07592   | 0.03600           | -0.20003     | 0.01511    | -0.00648               | 0.09015       | 0.00004
#   FB    | 0.26374  | -0.03220      | 0.03853  | 0.06166    | 0.01095     | 0.06777   | 0.18904        | 0.03280       | -0.26527  | -0.70040          | 0.12223      | -0.12200   | 0.16502                | -0.12761      | 0.38270
#   Total | 0.16632  | -0.09778      | 0.03161  | -0.00558   | 0.06580     | 0.12515   | 0.29369        | 0.08481       | -0.14792  | -0.39664          | 0.32173      | -0.16540   | 0.01383                | -0.09930      | 0.24567
#
########################################################################################################################################################################################################################################################

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
