########################################################################################################################################################################################################################################################
# 
# This function creates a table with the sensitivities weight exposures in % of a given portfolio on a bucket level, for a given period 
# of time for each stock in the portfolio. It also provides the portfolio total sensitivities weight exposures per bucket. 
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
#                   | Name | Weight  | L/S |
#                   | AAPL |   0.3   |  1  |
#                   | MSFT |   0.3   | -1  |
#                   | FB   |   0.4   |  1  |
#
#           * date - portfolio date (e.g. '2019-05-20') 
#
# Output: 
#         dataframe with the following columns:
#               * Column with all the portfolio stock names plus the 'Total' row - dataframe index. 
#               * A column per Bucket with its weight sensitivities in % associated to each stock in the portfolio. 
#               * e.g.
#
#         Corp credit| Country Growth|	DM FX   |  EM FX     | EM Sov Risk | Energy    | Est. Earnings  | Global Growth | Global QE | Global Real Rates | Infl. Expec. | Metals     | Peripheral EU Sov Risk | Risk Aversion | Systemic liquidity
#   AAPL |-0.066021  | -0.030483     | -0.002127|  -0.022194 | 0.009417    | 0.039957  | 0.031908       | 0.019335      | 0.012429  | 0.080328          | 0.119859     | -0.017553  | -0.043413              | -0.018552     | -0.041121
#   MSFT |0.036795   | 0.010809      | 0.000051 |  0.002022  | 0.007038    | -0.022743 | -0.000513      | -0.003732     | 0.022776  | 0.010800          | -0.060009    | 0.004533   | -0.001944	             | 0.027045      | 0.000012
#   FB	 |0.105496   | -0.012880     | 0.015412 |  0.024664  | 0.004380    | 0.027108  | 0.075616       | 0.013120      | -0.106108 | -0.280160         | 0.048892     | -0.048800  | 0.066008               | -0.051044     | 0.153080
#   Total|0.076270   | -0.032554     | 0.013336 |  0.004492  | 0.020835    | 0.044322  | 0.107011       | 0.028723      | -0.070903 | -0.189032	        | 0.108742     | -0.061820  | 0.020651               | -0.042551     | 0.111971     
#
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


def get_portfolio_sens_exposures_bucket(portfolio,date):
    
    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:

        stock_names = portfolio['Name']
        df_tot = pandas.DataFrame()
        rsq = []

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
                df_tot = pandas.concat([df_tot, df_sensitivities], axis = 0, join = 'outer')
                
            rsq.append(get_Rsq(stock, date, date, term)['Rsq'].values[0])

        df_rsq = pandas.DataFrame({'Rsq': rsq}, index = stock_names)
        portfolio_sensitivities = pandas.DataFrame({},columns = df_tot.columns)

        for stock in stock_names:

            portfolio_sensitivities.loc[stock] = [a*float(df_rsq['Rsq'][stock])/100*float(portfolio[portfolio['Name']==stock]['Weight'])*float(portfolio[portfolio['Name']==stock]['L/S']) for a in df_tot.loc[stock]]

        portfolio_sensitivities.loc['Total'] = [portfolio_sensitivities[x].sum() for x in portfolio_sensitivities.columns]

        portfolio_exposures = portfolio_sensitivities.loc[['Total']]

        return portfolio_sensitivities
