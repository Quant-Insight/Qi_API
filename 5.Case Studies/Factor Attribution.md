# Factor Attribution - Calculating Macro-Warranted Moves

Ingesting Qi data via the API enables quants to firstly identify they key factor sensitivities of any asset, & then, given the subsequent shift in those factors, calculate how effective macro has been in driving markets. Armed with this a quant can provide their portfolio managers with empirical attribution analysis across a range of financial asset classes.

https://www.quant-insight.com/stress-testing-covid-19-macro-explains-market-moves/

## Case Study: ‘Stress testing Covid-19: macro explains market moves’ – March 2020

* The impact of the Covid-19 crisis on financial markets has been profound. The lack of liquidity and gap risk makes execution extremely challenging. However, from a risk management perspective, most asset classes have behaved in a way that’s consistent with the huge macro shock the global economy has experienced.

*	By quantifying an asset's sensitivity to the dominant macro factors of the day, Qi’s model accuracy and its underlying methodology have been strongly validated.

* Only in European rates was the model undone by the severity of the rebound in yields after the early March low. Otherwise, given as asset's sensitivity to macro factors and the subsequent factor shifts, the accuracy of Qi’s models were reassuringly high.

*	Qi is uniquely positioned to provide a macro framework and risk solution that clients can use to prepare for the months ahead. Stress test your funds sensitivity to forthcoming macro shocks using our robust quantitative analytics.

Updating this since the original March analysis produces similar results. 

1.)	Macro does a very good job of explaining price action in both the initial Covid-19 shock, & in the subsequent recovery.

2.)	The key drivers for now remain largely the same – credit spreads, risk aversion & inflation are the macro themes every investor, across asset classes, needs visibility on.



<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/spx_covid_moves.png" alt="Case Study"/>
</br>


<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/spx_covid_factor_attribution_1.png" alt="Case Study"/>
</br>

* Code:

      # Requirements - make sure you've set environment variable QI_API_KEY = YOUR_API_KEY
      import Qi_wrapper
      import pandas

      # Function to pull relevant factor data (zscores & sensitivities)
      def get_factor_data(model,date,term):

          sensitivity = Qi_wrapper.api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)
          date = [x for x in sensitivity][0]
          df_sensitivities = pandas.DataFrame()

          for data in sensitivity[date]:
              df_sensitivities[str(data['driver_name'])]=[data['driver_zscore'], data['sensitivity']]

          df_sensitivities = df_sensitivities.T
          df_sensitivities.columns = ['z_score','Sensitivity']


          return df_sensitivities

      # Funtion to calculate macro factor attribution
      def get_factor_attribution(asset,start,end,start_price,end_price,term):

          factor_start = get_factor_data(asset,start,term) 
          factor_end = get_factor_data(asset,end,term)

          # Calculate the factor contribution in model deviations from mean, for each point in time
          end_data = (factor_end.z_score * factor_end.Sensitivity) * end_price/100   
          start_data = (factor_start.z_score * factor_start.Sensitivity) * start_price/100

          # Subtract the two to get your factor attributions
          factor_attribution = pandas.DataFrame(end_data - start_data)

          # Convert factors into macro buckets (e.g. Copper & Iron Ore --> Metals)
          sensitivity = Qi_wrapper.api_instance.get_model_sensitivities(model=asset,date_from=start,date_to=start,term=term)
          date = [x for x in sensitivity.keys()][0]
          df_bucket_names = pandas.DataFrame([x['bucket_name'] for x in sensitivity[date]],[x['driver_name'] for x in sensitivity[date]])
          bucket_attribution = pandas.DataFrame()

          for factor in factor_attribution.index:

              if df_bucket_names[0][factor] in bucket_attribution.columns:
                  bucket_attribution[df_bucket_names[0][factor]] = bucket_attribution[df_bucket_names[0][factor]] + factor_attribution[0][factor]

              else:
                  bucket_attribution[df_bucket_names[0][factor]] = [factor_attribution[0][factor]]


          return bucket_attribution.T


      # Choose asset
      asset = 'SPX'

      # Enter price of asset
      start_date = '2020-01-01'
      start_price = ###.##

      mid_date = '2020-03-23'
      mid_price = ###.##

      end_date = '2020-07-02'
      end_price = ###.##


      # Results for Covid crash
      covid_crash_factor_moves = get_factor_attribution(asset,start_date,mid_date, start_price, mid_price, 'Long Term')
      covid_crash_macro_warranted_move = covid_crash_factor_moves.sum().item()
      covid_crash_return_attributions = covid_crash_factor_moves[0] / start_price

      # Results for the rebound
      rebound_factor_moves = get_factor_attribution(asset,mid_date,end_date, mid_price, end_price, 'Long Term')
      rebound_macro_warranted_move = rebound_factor_moves.sum().item()
      rebound_return_attributions = rebound_factor_moves[0] / mid_price
