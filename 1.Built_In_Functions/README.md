# Built-in Functions

Our collection of built-in functions for the Qi_API. All of the output is in basic structures and requires unpacking in order to begin retrieving more specific items of data such as timeseries or sensitivity matrices. 

These are our basic API calls which are the building blocks for more complex analysis and data retrieval.


e.g for a specific model you can retrieve timeseries data but will require further unpacking to pull just the timeseries values for specific parameters:



e.g. 

      api_instance.get_model_timeseries('aapl')
      
Output:

{'_date': datetime.datetime(2020, 3, 16, 0, 0), <br>
'absolute_gap': ...,      (asset price - model value) <br>
'constant': ..., <br>
'fair_value': ...,      (Qi's model value) <br>
'percentage_gap': ...,   (% difference between the asset price and model value) <br>
'rsquare': ...,          (measure of model confidence) <br>
'sensitivities': None, <br>
'sigma': ...,            (Qi's valutaion gap (FVG))<br>
'target_mean': ...,     (Mean of asset price) <br>
'target_stdev': ...,     (Standard deviation of asset price) <br>
'target_zscore': ...,    (Z score of asset price) <br>
'zscore': ...            (Z score of model)}

