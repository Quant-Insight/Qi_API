# Built-in Functions

Our collection of built-in functions for the Qi_API. All of the output is in basic strucutres and requires unpacking in order to begin retrieving more specifc items of data such as timeseries or sensitivity matrices. 

These are our basic high-level calls which are the building blocks for more complex analysis and data retrieval.


e.g for a specific model you can retrive timeseries data but will require further unpacking to pull just the timeseries values for specific parameters:


e.g. 

api_instance.get_model_timeseries('aapl')

  'zscore': 0.69048}, {'_date': datetime.datetime(2020, 3, 16, 0, 0),
  'absolute_gap': -1.59068,
  'constant': 1.63222,
  'fair_value': 243.80068,
  'percentage_gap': -0.65674,
  'rsquare': 84.47174,
  'sensitivities': None,
  'sigma': -0.03708,
  'target_mean': 250.21928,
  'target_stdev': 42.90124,
  'target_zscore': -0.18669,
  'zscore': -0.14961}, {'_date': datetime.datetime(2020, 3, 17, 0, 0),
  'absolute_gap': -20.20668,
  'constant': 1.6259,
  'fair_value': 262.41668,
  'percentage_gap': -8.34263,
  'rsquare': 84.6299,
  'sensitivities': None,
  'sigma': -0.47296,
  'target_mean': 250.45627,
  'target_stdev': 42.72416,
  'target_zscore': -0.19301,
  'zscore': 0.27995}]

