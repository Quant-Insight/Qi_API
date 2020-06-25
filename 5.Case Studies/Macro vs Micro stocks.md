# Macro vs Micro – enabling stock pickers to identify when macro matters

The example below is aimed at bottom-up stock pickers. It shows how Qi data can be presented in a way to give stock-picking portfolio managers an immediate sense of when their normal analysis of company fundamentals is the dominant driver of equity prices; and therefore it is ‘busines as usual’, and those times when macro factors are the dominant narrative driving financial markets.

The code below provides an example to show quants how they can present Qi data to their equity portfolio managers. This example focuses on Asian single stocks but this kind of search can be replicated across asset classes and across geographies.


## Case Study: 'Asian single stocks' – June 2020

Qi uses 65% model confidence as our threshold for a macro regime. Any dot to the right of that vertical 65% bound is deemed to be in a macro regime. Plots to the left are being driven by non-macro factors. For bottom up stock pickers that means a continuation of their analysis of micro company fundamentals.

The y-axis shows Qi’s Fair Value Gap measure: how far a stock is from macro-warranted model value. Red dots north of the horizontal zero bound are rich to macro model; green dots below are cheap to macro. 


* So macro model confidence on Softbank here is 10% - Softbank is not about macro factors. 

* Kia Motors is in a strong macro regime (RSq 88%) and it is modestly rich versus model, +0.4 sigma above model value.

* Samsung is also in a strong macro regime (72% model confidence) but it is cheap to its macro environment, -1.3 sigma below model.

In one visual you can manipulate the data to quickly show an equity PM where their normal investment process works, and where they may need to add a macro overlay.

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/macro_vs_micro_stocks_2.PNG" alt="Case Study"/>
</br>

* Code:

      # Requirements - make sure you've set environment variable QI_API_KEY = YOUR_API_KEY
      import Qi_wrapper
      import pandas

      #Set universe and variables
      universe = [x.name for x in Qi_wrapper.api_instance.get_models(tags = 'Asia')][::2]
      date = '2020-06-24'    
      term = 'Long Term'

      # Create empty dataframe to be filled
      df_ = pandas.DataFrame(index = universe)

      # Get asset names
      df_['Name'] = [Qi_wrapper.api_instance.get_model(stock).security_name for stock in df_.index]

      fvgs = []
      RSqs = []

      for stock in df_.index:

          # Pull data with the Qi wrapper
          data = Qi_wrapper.get_model_data(stock,date,date,term)

          # Only interested in stocks with data for this date, drop the rest
          if len(data) > 0:
              fvgs.append(float(data.FVG))
              RSqs.append(float(data.Rsq))

          else:
              df_.drop(stock,axis = 'index',inplace=True)

      df_['FVG'] = [round(x,2) for x in fvgs]
      df_['RSq'] = [round(x,1) for x in RSqs]

      # Set colours (green for cheap & red for rich)
      df_['color'] = ['green' if x < 0 else '#C3423F' for x in df_.FVG]

      # Set strength of colour (reduced for low RSq)
      df_['opacity'] = [0.5 if x < 65 else 1 for x in df_.RSq]

      # Plot the data in the resulting dataframe - df_
