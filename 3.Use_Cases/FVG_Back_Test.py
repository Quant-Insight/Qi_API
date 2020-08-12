#######################################################################################################################################################################################################################################################
#######################################################################################################################################################################################################################################################
# 
# This function back-tests Qi's FVGs and computes the profitability of their signals.
#
# Requirements:
#         import pandas
#         import Qi_wrapper
#         import numpy as np
#
# Inputs: 
#           * price_data - a dataframe of your asset price data,
#             must be in the following format:
#
#                   |            | AAPL US Equity | A US Equity |
#                   | 2019-01-02 |     ##.##      |   ##.##     |
#                   | 2019-01-03 |     ##.##      |   ##.##     |
#                   | 2019-01-04 |     ##.##      |   ##.##     |
#                              
#             The dates must be the index of the dataframe, and have the format 'YYYY-MM-DD'                  
#               
#
#            * assets - a list of the assets you want to back-test e.g. ['AAPL US Equity,'A US Equity']
#            * open_arg - the absolute value the FVG needs to be to open a trade e.g. 1.0
#            * close_arg - the absolute value the FVG needs to be to close a trade e.g. 0.25
#            * rsq_arg - the value the RSq needs to be to open a trade e.g. 65
#            * l_s - specify the trading strategy; ['Long'], ['Short'] or ['Long','Short']
#            * start_date - specify the date to start the back-test e.g. '2019-01-02'
#            * end_date - specify the date to end the back-test e.g. '2020-01-02'
#            * term - chose between 'Short Term' or 'Long Term' Qi data
#
#
# Example of call: fvg_back_test(['AAPL US Equity','A US Equity'],price_data,1.0,0.25,65,['Long','Short'],'2009-01-02','2019-01-04','Long Term')
# 
# Output: 
#
#                       | Results |
#   Hit Rate            |  72.5   |
#   Avg. Rtrn           |  1.46   |  
#   Avg. Holding Period |  25.7   |    
#   No. of Trades       |   40    |    
#   Avg. Win            |  4.70   |
#   Avg. Loss           | -7.81   |
#   Win/Loss            |  0.60   |
#
#
#
########################################################################################################################################################################################################################################################


def fvg_back_test(assets,price_data,open_arg,close_arg,rsq_arg,l_s,start_date,end_date,term):

    # Create empty lists for results
    Holding_Times = []
    ALL_returns = []
    Name = []
    Date = []
    LongShort = []
    trade_RSq = []
    trade_FVG = []
    CloseDate = []
    
    # Convert tickers to Qi model names 
    model_names = Qi_wrapper.get_model_names_from_tickers(assets)
    
    for asset in assets:    

        model_name = model_names['Qi Model Name'][asset]
        
        # If no Qi model matches a ticker
        if model_name == None:
            print(asset + ': Ticker not found in any Qi Model')
            
        # Otherwise continue to test FVGs
        else:
        
            # Pull model data from API and price data from your csv
            data = Qi_wrapper.get_model_data(model_name,start_date,end_date,term)
            price = price_data[asset]
            
            # Find common dates between the two data sets, and only consider those
            common_dates = [date for date in data.index if date in price.index]
            data = data.loc[common_dates]
            price = price.loc[common_dates]
            
            FVG = data['FVG']
            RSq = data['Rsq']

            # Find potential times to close a trade
            FVG_closelong = FVG>-1*close_arg
            FVG_closeshort = FVG<close_arg


            i = 0

            while i < (len(FVG)):

                # Longs
                if 'Long' in l_s and FVG[i] < -1*open_arg and (FVG_closelong[i:] == True).sum() > 0 and RSq[i] > rsq_arg:

                    # Find open & close dates for the trade
                    new_price_index = FVG_closelong.tolist().index(True,i,len(FVG))
                    close_date = str(FVG.index[new_price_index])[:10]
                    open_date = str(FVG.index[i])[:10]

                    # Calculate returns & holding period
                    returns = ((price[close_date] - price[open_date])/price[open_date])*100   
                    TradeLength = new_price_index - i
                    Holding_Times.append(TradeLength)

                    # Add trade info to results
                    Name.append(asset)
                    Date.append(open_date)   
                    ALL_returns.append(returns)
                    LongShort.append('Long')
                    CloseDate.append(close_date)
                    trade_RSq.append(RSq[i])
                    trade_FVG.append(FVG[i])

                    # Only open one trade in any asset at one time, so skip to end of trade
                    i = new_price_index + 1

                    
                # Shorts
                elif 'Short' in l_s and FVG[i] > open_arg and (FVG_closeshort[i:] == True).sum() > 0 and RSq[i] > rsq_arg:

                    new_price_index = FVG_closeshort.tolist().index(True,i,len(FVG))
                    close_date = str(FVG.index[new_price_index])[:10]
                    open_date = str(FVG.index[i])[:10]

                    returns = (-(price[close_date] - price[open_date])/price[open_date])*100   
                    TradeLength = new_price_index - i
                    Holding_Times.append(TradeLength)

                    Name.append(asset)
                    Date.append(open_date)   
                    ALL_returns.append(returns)
                    LongShort.append('Short')
                    CloseDate.append(close_date)
                    trade_RSq.append(RSq[i])
                    trade_FVG.append(FVG[i])

                    i = new_price_index + 1

                else:            
                    i = i + 1

    
    # Calculate results metrics
    HitRate = 100*sum([x > 0 for x in ALL_returns])/len(ALL_returns)
    AverageProfit = np.mean(ALL_returns)
    AverageHolding = np.mean(Holding_Times)
    mean_win = np.mean([x for x in ALL_returns if x > 0])
    mean_loss = np.mean([x for x in ALL_returns if x < 0])
    mean_win_loss_ratio = mean_win/(-1*mean_loss)
    # trades_per_day = len(ALL_returns)/len(FVG)
    number_of_trades = len(ALL_returns)

    results = [HitRate,AverageProfit,AverageHolding,number_of_trades,mean_win,mean_loss,mean_win_loss_ratio]
    
    ### Uncomment below to return a summary of results
    
    df_results = pandas.DataFrame(results,index = ['Hit Rate','Avg. Rtrn','Avg. Holding Period','No. of Trades','Avg. Win',
                                     'Avg. Loss','Win/Loss'], columns = ['Results'])
    
    ### Uncomment below to return all individual trades
    
#     df_results = pandas.DataFrame({'Asset':Name,'Entry Date':Date,'Exit Date':CloseDate,'Returns':ALL_returns,'Duration':Holding_Times,
#                                   'Type':LongShort,'FVG':trade_FVG,'RSq':trade_RSq})
    
    return df_results
