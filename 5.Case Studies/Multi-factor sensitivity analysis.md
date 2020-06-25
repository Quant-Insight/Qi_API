# Multi-factor sensitivity analysis – stress test specific scenarios

Portfolio managers will often identify potential scenarios which could potentially impact their risk. Using Qi data, a quant can arm his PMs with an empirical stress test for a number of different macro scenarios.

In this instance we look at US equity markets (the S&P500) in the aftermath of the Covid-19 shock to the US economy. A key dilemma facing equity managers was ascertaining which was the dominant driver of markets – the huge deflationary shock from the pandemic versus the massive policy response from authorities.

Qi can show the independent impact of different factors on an asset & here we constructed a measure of that growth vs liquidity trade-off. However this analysis could be run for a number of factors – wider credit spreads, higher crude oil prices, spikes in VIX – and on a range of different assets around the globe.

## Case Study: 'Growth vs Liquidity – What’s driving SPOOs?' - June 2020

* Periods in red denote times when the biggest driver of the S&P500 were changes in economic growth and inflation. Those occasions when Fed monetary policy became the dominant driver are captured in blue. 

* For most of the last year, the fundamental economic backdrop explained changes in US equity markets. That changed sharply in Q1 2020. Liquidity first become the bigger driver at the end of February; and by late March was significantly more important in determining price action in US equity markets.


<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/growth_vs_policy.PNG" alt="Case Study"/>
</br>

* Code:

      # Requirements - make sure you've set environment variable QI_API_KEY = YOUR_API_KEY
      import Qi_wrapper
      import pandas
      
      # Set variables
      asset = 'SPX'
      date = '2020-06-24'
      date_1y = '2019-06-24'
      term = 'Short Term'

      # Pull historical sensitivities with Qi wrapper
      df_sensitivities = Qi_wrapper.get_sensitivity_grid(asset,date_1y, date,'Short Term')

      # Create growth sensitivitiy timeseries
      growth_sensitivity = df_sensitivities[['US GDP', 
                                             'US 2y Infl. Expec.', 
                                             'US 5y Infl. Expec.', 
                                             'US 10y Infl. Expec.']].sum(axis=1)

      # Create policy sensitivitiy timeseries
      policy_sensitivity = df_sensitivities[['US HY', 
                                             'FED QT Expectations', 
                                             'FED rate expectations']].sum(axis=1) - df_sensitivities['EUR 1y Basis Swap']

      # Calculate the spread of the absolute timeseries
      growth_policy_spread = abs(growth_sensitivity) - abs(policy_sensitivity)
