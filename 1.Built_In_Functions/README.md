# Built-in Functions

Our collection of built-in functions for the Qi_API. All of the output is in basic strucutres and requires unpacking in order to begin retrieving more specifc items of data such as timeseries or sensitivity matrices. 

These are our basic API calls which are the building blocks for more complex analysis and data retrieval.


e.g for a specific model you can retrive timeseries data but will require further unpacking to pull just the timeseries values for specific parameters:


e.g. 

      api_instance.get_model_timeseries('aapl')

   {'_date': datetime.datetime(2020, 3, 16, 0, 0), <br>
  'absolute_gap': -1.59068, <br>
  'constant': 1.63222, <br>
  'fair_value': 243.80068, <br>
  'percentage_gap': -0.65674, <br>
  'rsquare': 84.47174, <br>
  'sensitivities': None, <br>
  'sigma': -0.03708, <br>
  'target_mean': 250.21928, <br>
  'target_stdev': 42.90124, <br>
  'target_zscore': -0.18669, <br>
  'zscore': -0.14961}

