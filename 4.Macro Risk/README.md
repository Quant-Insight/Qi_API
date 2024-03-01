# Macro Risk

Qi enables users to identify their exposure to critical macro factors. Below we identify some of the key functions Qi Macro Risk can provide. We show examples of code to help quants run their own analysis; and ideas of how to best present the data for risk managers.

These incude:
* Exposure to macro factors, on a line-by-line basis across holdings, in both standard deviation and cash terms.
* Attribution analysis.
* Relative performance versus a chosen benchmark.
<br>
Requirements:
<br>

      %set_env QI_API_KEY = YOUR_API_KEY
      import Qi_wrapper
      import pandas
      import numpy as np 

      ### Set Variables
      benchmark_name = 'S&P500'
      date = '2024-02-23'
      term = 'Long Term'
      
      ### Create portfolio (alternatively import a csv with the same format)
      portfolio = pandas.DataFrame({'Name':['MSFT','GOOG','PG','JPM','AAPL','META','GS','MRO','DEI','SO'],
                  'Position':[194300000,142000000,122440000,122440000,113940000,109690000,106290000,102040000,102040000,99060000]})

      portfolio['Weight'] = [abs(x)/sum(abs(portfolio.Position)) for x in portfolio.Position]
      portfolio['L/S'] = [1]*len(portfolio)
      
<br>

Portfolio:

   <br>
   <p align="center">
   <img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/portfolio_new.png" alt="Portfolio Table"/>
   </p>
   </br>


## Calculate cash exposures

Factor cash exposures are derived by multiplying individual stock's notional amounts to their factor sensitivities. For example in the table below, if energy prices were to rise by 1 standard deviation, the value of your position in Microsoft (MSFT) would increase by $288,963, and the value of your portfolio as a whole would increase by $2,744,827. These values are calculated on the bucket level, where each bucket can contain up to 4 individual macro factors, e.g. the bucket 'Metals' contains the factors copper and iron ore.

      Qi_wrapper.get_portfolio_cash_exposures_bucket(portfolio,date,term)
      
<br>
Output:
<br>

   <br>
   <p align="center">
   <img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/cash_exposures_new.png" alt="Cash table"/>
   </p>
   </br>
   
   
## Get portfolio sensitivities to top 10 individual macro buckets
   
Compute the expected % change in value of a portfolio for a 1 standard devation move in each of the top 10 macro factors.
   
      sens = Qi_wrapper.get_portfolio_sens_exposures_bucket(portfolio,date,term)
      sens[abs(sens.loc['Total']).nlargest(10).index].loc[['Total']]
      
   
<br>
Output:
<br>

   <br>
   <p align="center">
   <img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/portfolio_exposures_new.png" alt="Sens table"/>
   </p>
   </br>
   
   
   ## Plot pie chart of portfolio's macro factor breakdown
   
      ### Create pie chart data  
      import numpy as np

      sens_buckets = Qi_wrapper.get_portfolio_sens_exposures_bucket(portfolio,date,term)
      pie_data = sens_buckets.loc[['Total']].T.sort_values(by='Total')[::-1]
      pie_data.Total = [abs(x)/abs(pie_data).Total.sum() for x in pie_data.Total]
      
      
      ### Create plot

      import matplotlib.pyplot as plt

      labels = pie_data.index
      sizes = pie_data.Total
      fig1, ax1 = plt.subplots(figsize=(15, 12))

      ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
              shadow=False, startangle=90)
      ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

      plt.show()
      
   
<br>
Output:
<br>

   <br>
   <p align="center">
   <img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/pie_chart_new.png" alt="pie chart"/>
   </p>
   </br>


 ## Plot portfolio sensitivities relative to a benchmark
   
      ### Creates data for plot
      sens_buckets = Qi_wrapper.get_portfolio_sens_exposures_bucket(portfolio,date,term)
      bar_plot_data = sens_buckets.loc[['Total']].T.sort_values(by='Total')[::-1]
      benchmark = Qi_wrapper.get_bucket_drivers(benchmark_name,date,term)
      idxs = bar_plot_data.index.tolist()
      bar_plot_data[benchmark_name] = benchmark[idxs].T.Sensitivity
   
      ### Create plot
      fig = plt.figure(figsize=(15, 8))
      ax = fig.add_subplot(111)
      ax.spines["top"].set_visible(False)  
      ax.spines["right"].set_visible(False)
      ax.bar(bar_plot_data.index,bar_plot_data.Total,zorder=1)
      ax.scatter(bar_plot_data.index,bar_plot_data['S&P500'],zorder=2,color='red')
      plt.xticks(rotation='vertical')
      plt.ylabel('% Chng in Portfolio for a 1std move in Factor',size=12)
      plt.legend([benchmark_name,'Fund'])
      plt.show()
      
   
<br>
Output:
<br>

   <br>
   <p align="center">
   <img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/bar_chart_new.png" alt="portfolio vs benchmark"/>
   </p>
   </br>
