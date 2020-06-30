# Regime shifts – a volatility signal

Building on the analysis in ‘Regime Shifts’ detailing the emergence of new macro regimes, quants can also use Qi model confidence data to flag potential volatility events. In this instance we look at sharp falls in model RSq which can give portfolio managers an early indication of sudden shifts in fundamentals that often presages a spike in volatility.

We provide two examples of such events & the code to enable a quant to best showcase this functionality.

## Case Study 1 – an early warning ahead of Covid-19, Jan 2020

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/rsq_plot1.png" alt="Case Study"/>
</br>

Major equity indices around the globe saw a sharp fall in model confidence in January. At the time, equities were making fresh highs and Covid-19 was deemed a uniquely Chinese problem. The sudden fall in macro’s ability to explain moves in global equity markets was a flag that a regime shift was taking place and that new highs in equities were not consistent with macro fundamentals.
 
## Case Study 2 – flagging “Volmageddon”, Jan 2018

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/rsq_plot2.png" alt="Case Study"/>
</br>

Macro’s ability to explain shifts in all assets fell sharply at the end of 2017. When equity, bond & currency markets are all moving independent of economic fundamentals, financial conditions and risk appetite that is a warning that markets have divorced themselves from ‘reality’. 

Testing the idea that sharp falls in Qi RSq could be used as a vol signal, the chart below, the blue line shows the % of Qi models for major, cross asset benchmarks (equities, rates, FX, credit, cmdties, DM & EM) with RSq below our 65% threshold.
 
A sharp move up in the blue line signals a large proportion of major markets are dropping below the 65% RSq threshold. We overlaid with VIX.
 
It works on the way up, but VIX moves back down much faster that RSq’s go back up.
 
We concluded, a sharp & broad RSq drop is useful in flagging upcoming vol events. However, RSq is too slow to signal the end of the vol episode; VIX moves down well before RSqs gets back above 65%.

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/vix and RSq.png" alt="Case Study"/>
</br>

* Code:

      # Requirements - make sure you've set environment variable QI_API_KEY = YOUR_API_KEY
      import Qi_wrapper
      import pandas
      
      # Function to get multiple asset RSqs
      def get_asset_rsqs(assets,start,end,term):

          rsq_data = pandas.DataFrame()

          for model in assets:
              data = Qi_wrapper.get_model_data(model,start,end,term)
              rsq_data[model] = data['Rsq']

          return rsq_data


      # Case study 1
      models_1 = ['AS51', 'NDX', 'NKY', 'RTY', 'SPX']
      results_1 = get_asset_rsqs(models_1,'2019-01-01','2020-01-10','Long Term')


      # Case study 2
      models_2 = ['SPX', 'SXXP', 'EURUSD', 'USDJPY', 'USD 10Y', 'EUR 10Y']
      results_2 = get_asset_rsqs(models_2,'2017-10-02','2018-01-09','Long Term')
