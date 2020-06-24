# Factor sensitivity with a valuation overlay

The example below details how clients can use Qi data via our API to screen assets for the largest sensitivity to a given factor. In this instance we look at which global equity indices are most sensitivie to USDCNH, see the article: https://www.quant-insight.com/usdcnh-implications-for-risky-assets/ .


Again, this kind of search could be replicated across multiple asset classes & for numerous macro factors.


The code below provides an example for quants looking to manipulate the data. The bullet point summary is one suggestion of how to present the results for a portfolio manager looking for optimal trade selection, or a risk manager searching for visibility on their macro exposures.

## Case Study: 'USDCNH – Implications for risky assets' - May 2020

* The Trump White House appears to be ratchetting up the pressure on China around the Covid-19 outbreak. Political analysis suggests this could be a feature of the election campaign.

* From a financial market perspective, that’s prompting a renewed rally in USDCNH. A stronger USD / weaker Yuan is typically associated with ‘risk off’ but, more specifically, which assets are most vulnerable ? Qi can empirically observe the independent sensitivity of any asset to USDCNH. 

* The table below screens global equity indices for those most sensitive to a one standard deviation increase in USDCNH, holding every other factor constant. Models not in a macro regime (RSq < 65%) are screened out and then we simply rank the top 10.

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/Indices - USDCNH (May 2020).PNG" alt="Case Study"/>
</br>

* Code:

      # Requirements - make sure you've set environment variable QI_API_KEY = YOUR_API_KEY
      import Qi_wrapper
      import pandas

      # Set varialbles and universe 
      factor = 'USDCNH'
      date = '2020-05-01'
      term = 'Long Term'
      universe = [x.name for x in Qi_wrapper.api_instance.get_models(tags = 'Indices')][::2]

      RSq_data = []
      factor_data = []
      names = []
      FVGs = []

      for asset in universe:

          # Pull data from API using Qi wrapper
          model_data = Qi_wrapper.get_model_data(asset,date,date,term)
          RSq = model_data['Rsq'].item()
          FVG = model_data['FVG'].item()
          sensitivities = Qi_wrapper.get_factor_drivers(asset,date,term).T

          if factor in sensitivities.columns:
              factor_sens = sensitivities[factor].item()
          else:
              factor_sens = None

          RSq_data.append(RSq)
          FVGs.append(FVG)
          factor_data.append(factor_sens)
          names.append(Qi_wrapper.api_instance.get_model(asset).security_name)

      factor_df = pandas.DataFrame({'Name':names,factor+' %':factor_data,'RSq':RSq_data,'FVG':FVGs}, index = universe)

      # Set result constraints
      RSq_constraint = 65
      result_size = 10

      # Compile results
      top_names = abs(factor_df[factor_df['RSq']>RSq_constraint][factor+' %']).nlargest(result_size).index
      final_df = factor_df.loc[top_names]
      
      
