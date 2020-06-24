# Regime shifts

The example below details how clients can use Qi data via our API to identify assets undergoing large macro regime shifts. Qi uses a measure called R-squared (RSq) to measure a model's macro explanatory power. Large movements in RSq denote a significant change in the macro regime of an asset. In this instance we look at which global equity indices have had the biggest recent change in RSq, see the article: https://www.quant-insight.com/can-you-afford-not-to-know/ .

The code below shows how Qi manipulated the data to generate these results, and should be of use to any quants who want to repeat this exercise, or incorporate into their own use-case. The bullet point summary shows how a Qi analyst has interpreted the results 

## Case Study: 'Can you afford not to know' - March 2020

* Macro’s ability to explain shifts in European equity indices is increasing dramatically

* The critical drivers of European equities are risk aversion and credit spreads. 

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/rsq_changes.PNG" alt="Case Study"/>
</br>

* The chart above is the result of looking at all Qi’s Long Term models across global equity indices and identifying the 10 with the biggest R-Squared change over the last month; whether those changes are positive or negative. Equity indices globally all posted strong increases in RSq, i.e. macro’s explanatory power has improved dramatically of late. Seven of the top 10 are European indices.

* The table below lists the top drivers of these new macro regimes. Two factors emerge across all models – the desire for lower risk aversion and tighter credit spreads.

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/rsq_changes_table.PNG" alt="Case Study"/>
</br>

* Code:

      # Requirements - make sure you've set environment variable QI_API_KEY = YOUR_API_KEY
      import Qi_wrapper
      import pandas
      from datetime import datetime,timedelta


      # Set universe and varialbles
      universe = [x.name for x in Qi_wrapper.api_instance.get_models(tags = 'Indices')][::2]
      term = 'Long Term'


      # Get date for most recent data point 
      if datetime.today().weekday() == 0:
          date = datetime.now() - timedelta(3)
      # If today is Sunday, we retrieve data from previous Friday. 
      elif datetime.today().weekday() == 6:
          date = datetime.now() - timedelta(2)
      # otherwise, we retrieve data from the previous day. 
      else:
          date = datetime.now() - timedelta(1)

      date = date.strftime('%Y-%m-%d')


      # Get date for 1 month ago
      date_1m = datetime.now().date() - timedelta(days=30)

      # If a weekend, move day back to Friday
      if date_1m.weekday() == 5:
          date_1m = date_1m - timedelta(days=1)
      elif date_1m.weekday() == 6:
          date_1m = date_1m - timedelta(days=2)
      else:
          date_1m = date_1m

      date_1m = date_1m.strftime('%Y-%m-%d')

      # Create empty arrays    
      Rsq_array = []
      rsq_1m_array = []
      assets = []

      for asset in universe:

          # Pull R-Squared data using Qi wrapper
          rsq_now = Qi_wrapper.get_Rsq(asset,date,date,term)
          rsq_1m = Qi_wrapper.get_Rsq(asset,date_1m,date_1m,term)

          if (len(rsq_now) > 0) and (len(rsq_1m) > 0):
              Rsq_array.append(float(rsq_now['Rsq']))
              rsq_1m_array.append(float(rsq_1m['Rsq']))

              assets.append(asset)


      df_Rsq = pandas.DataFrame({'Rsq':Rsq_array,'Rsq-1m':rsq_1m_array,
                                 'Change':[x-y for x,y in zip(Rsq_array,rsq_1m_array)]},index = assets)

      # Find the 10 assets with the largest R-Squared 1m change
      df_final = df_Rsq.nlargest(10,'Change')


      # For these 10 assets, find the top 3 macro buckets which affect these models
      top_3_buckets = pandas.DataFrame(columns = ['Driver 1', 'Sens 1', 'Driver 2', 'Sens 2', 'Driver 3', 'Sens 3'])

      for asset in df_final.index:

          # Pull bucket sensitivity values using Qi wrapper
          bucket_drivers = Qi_wrapper.get_bucket_drivers(asset,date,term)

          T3_df = bucket_drivers[abs(bucket_drivers).T.nlargest(3,'Sensitivity').index]
          idx = T3_df.columns
          new_df = pandas.DataFrame([idx[0],round(float(T3_df[idx[0]]),2),idx[1],round(float(T3_df[idx[1]]),2),idx[2],round(float(T3_df[idx[2]]),2)],
                                    index = ['Driver 1', 'Sens 1', 'Driver 2', 'Sens 2', 'Driver 3', 'Sens 3'], columns = [asset])
          new_df = new_df.T

          new_df.index = [asset]

          # after final iteration, top_3_buckets will contain the top 3 bucket sensitivities for the 10 assets with the largest R-Squared 1m change
          top_3_buckets = top_3_buckets.append(new_df)
      
      
