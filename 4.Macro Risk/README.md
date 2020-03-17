# Macro Risk

Here we showcase how Qi uses the API to produce a Portfolio Macro Risk report.

* Requirements:
      %set_env QI_API_KEY = YOUR_API_KEY
      import QI_API_Library
      import pandas
      import numpy as np 
      
      ### Set Variables
      benchmark_name = 'SPX'
      date = '2020-03-16'
      term = 'Long Term'
      
      ### Create portfolio (alternatively import a csv with the same format)
      portfolio = pandas.DataFrame({'Name':['MSFT','GOOG','PG','JPM','NESN','SIE','WMT','CAT','AAPL','AZN'],
            'Position':[194300000,142000000,122440000,122440000,113940000,109690000,106290000,102040000,102040000,99060000]})
                  
      portfolio['Weight'] = [abs(x)/sum(abs(portfolio.Position)) for x in portfolio.Position]
      portfolio['L/S'] = [1]*len(portfolio)
      
<br>

Portfolio:

   <br>
   <p align="center">
   <img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/portfolio table.png" alt="Case Study 1"/>
   </p>
   </br>


## Case Study 1: '10 EU Stocks Vulnerable to deflation' - Mar 2020

* Back in mid February with Western equity markets seemingly immune, the key question facing a European long/short equity fund was which stocks are most vulnerable should Covid-19 spread and unleash a deflationary shock in this time zone? 

* On February 17th , the last week of complacency before the virus reached these shores, we screened the Stoxx 600 universe for those single names most sensitive to European inflation expectations, 

* The 10 stocks Qi identified as most sensitive to inflation fell 43% from February 17th to yesterday’s close. Over the same period, the Euro Stoxx 600 fell 34%.

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/EU stocks - infl (Mar 2020).png" alt="Case Study 1"/>
</br>

* Code:

      ### Variables ###
      universe = [x.name for x in api_instance.get_models(tags='Stoxx Europe 600')][::2]
      date = '2020-02-17'
      term = 'Long Term'
      driver_rank = 7   # The factor has to feature in the top 7 factors for an asset for it to be considered
      no_of_stocks = 10
      factor = 'Euro 5y Infl. Expec.'

      df = pandas.DataFrame()

      for asset in universe:

          try:

              df_temp = get_factor_drivers(stock,date,term).T
              df_temp.index = [asset]        

              if factor in abs(df_temp.loc[asset]).nlargest(driver_rank).index:

                  df = df.append(df_temp)

          except IndexError:

              pass

      df_factor = df[[factor]]
      df_factor['RSq'] = [float(get_model_data(asset,date,date,'Long Term')['Rsq']) for asset in df_factor.index]
      df_top_sensitivite = df_factor[df_factor['RSq']>65].nlargest(no_of_stocks,factor)
      df_top_sensitivite['Name'] = [api_instance.get_model(model).security_name for model in df_top_sensitivite.index]   
      
      
<br>
*Output:

  <br>
  <img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/EU stocks table - infl (Mar 2020).png" alt="Case Study 1 Table"/>
  </br>
