#######################################################################################################################################################################################################################################################
# 
# This function creates a table with the cash exposures of a given portfolio on a bucket level, for a given period of time for each 
# stock in the portfolio, weighted by the asset's model confidence (RSq). It also provides the portfolio total cash exposures per bucket. 
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
#                              'Position':[1000000, -1000000, 1000000]})
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
#                   | Name | Position  |
#                   | AAPL |   1000000 |
#                   | MSFT |  -1000000 |
#                   | FB   |   1000000 |

#           * date - portfolio date (e.g. '2019-05-20') 
#
# Output: 
#         dataframe with the following columns:
#               * Column with all the portfolio stock names plus the 'Total' row - dataframe index. 
#               * A column per Bucket with its chash sensitivities associated to each stock in the portfolio. 
#               * e.g.
#
#         | Corp credit | DM FX | EM FX  | EM Sov Risk | Energy | Est. Earnings | Global Growth | Global Real Rates | Infl. Expec. | Metals  | Peripheral EU Sov Risk | QT Expectations | Risk Aversion | Systemic liquidity | Yield Curve Slope
#   AAPL  | -2099.4     | -60.9 | -760.8 | 341.4       | 1559.3 | 1074.7        | -219.1        | 2257.8            | 4573.0       | -827.3  | -1441.7                | 99.4            | -901.3        | -1012.0            | -1166.9
#   MSFT  | 1266.5      | -16.3 | 71.8   | 225.0       | -631.4 | -9.4          | -286.2        | 592.1             | -2393.1      | 240.2   | -61.5                  | 909.3           | 1073.9        | -126.8             | 457.7
#   FB    | 2695.6      | 477.6 | 563.4  | 394.1       | -166.8 | 2079.7        | 1765.7        | -7072.8           | 2003.0       | -1270.4 | 1310.1                 | -2260.5         | -1188.5       | 3623.8             | -564.2
#   Total | 1862.7      | 400.4 | -125.6 | 960.5       | 761.1  | 3145.0        | 1260.4        | -4222.9           | 4182.9       | -1857.5 | -193.1                 | -1251.8         | -1015.9       | 2485.0             | -1273.4

########################################################################################################################################################################################################################################################

def get_Rsq(model, start, end, term):
    
    #Note that we only have data from Monday to Friday.
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')    
    
    if (start_date.weekday() == 5 or start_date.weekday() == 6) and (end_date.weekday() == 5 or end_date.weekday() == 6) and ((end_date - start_date).days == 1):
        print('Please choose a period of time which includes days between Monday and Friday.')
    else: 
        # Note that this may be more than 1 year of data, so need to split requests
        year_start = int(start[:4])
        year_end = int(end[:4])
        time_series = []
    
        for year in range(year_start, year_end + 1):
            query_start = start
            if year != year_start:
                date_from = '%d-01-01' % year
            else:
                date_from = start
            if year != year_end:
                date_to = '%d-12-31' % year
            else:
                date_to = end

            time_series += api_instance.get_model_timeseries(
            model,
            date_from=date_from,
            date_to=date_to,
            term=term)

        rsq = [data.rsquare for data in time_series]
        dates = [data._date for data in time_series]
        df = pandas.DataFrame({'Dates': dates, 'Rsq': rsq})
        df.set_index('Dates', inplace=True)

        return df


def get_portfolio_cash_exposures_bucket(portfolio,date,term):

    stock_names = portfolio['Name']
    df_tot = pandas.DataFrame()
    rsq = []

    for stock in stock_names:

        sensitivity = api_instance.get_model_sensitivities(model=stock,date_from=date,date_to=date,term=term)
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
            df_tot = pandas.concat([df_tot, df_sensitivities], axis = 0, join = 'outer')
        
        rsq.append(get_Rsq(stock, date, date, term)['Rsq'].values[0])
            
    df_rsq = pandas.DataFrame({'Rsq': rsq}, index = stock_names)        
    portfolio_sensitivities = pandas.DataFrame({},columns = df_tot.columns)
    
    for stock in stock_names:

        portfolio_sensitivities.loc[stock] = [a*float(df_rsq['Rsq'][stock])/100*float(portfolio[portfolio['Name']==stock]['Position'])/100 for a in df_tot.loc[stock]]

    portfolio_sensitivities.loc['Total'] = [portfolio_sensitivities[x].sum() for x in portfolio_sensitivities.columns]
    
    portfolio_exposures = portfolio_sensitivities.loc[['Total']]
    
    return portfolio_sensitivities
