# Built-in Functions

Our collection of built-in functions for the Qi_API. All of the output is in basic strucutres and requires unpacking in order to begin retrieving more specifc items of data such as timeseries or sensitivity matrices. 

These are our basic API calls which are the building blocks for more complex analysis and data retrieval.


e.g for a specific model you can retrive timeseries data but will require further unpacking to pull just the timeseries values for specific parameters:


e.g. 

      api_instance.get_model_timeseries('aapl')
      
Output:

{'_date': datetime.datetime(2020, 3, 16, 0, 0), <br>
'absolute_gap': -1.59068,      # asset price - model value <br>
'constant': 1.63222, <br>
'fair_value': 243.80068,      # Qi's model value <br>
'percentage_gap': -0.65674,   # % difference between the asset price and model value <br>
'rsquare': 84.47174,          # measure of model confidence <br>
'sensitivities': None, <br>
'sigma': -0.03708,            # Qi's valutaion gap (FVG)<br>
'target_mean': 250.21928,     # Mean of asset price <br>
'target_stdev': 42.90124,     # Standard deviation of asset price <br>
'target_zscore': -0.18669,    # Z score of asset price <br>
'zscore': -0.14961            # Z score of model}

