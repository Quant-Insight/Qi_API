## Description

This piece of code retrieves the historical factor sensitivities for a given model (USDJPY), a given period of time (between
2015-01-01 and 2019-01-10), given factors (1y1y Rate Diff., 2y2y Rate Diff. and 5y5y Rate Diff.), and a given term (Long Term). 

**Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** For the purpose of this example, the model, the factors, the period of time and the term are already defined in 
example_historical_factor_sensitivities() function. 
               
**Output:** A line chart representing 1y1y Rate Diff., 2y2y Rate Diff. and 5y5y Rate Diff. long term historical sensitivities 
for USDJPY, between 2015-01-01 and 2019-01-10.
               

## Code

```python
import qi_client
import pandas
from datetime import datetime

# Configure API key authorization: QI API Key
configuration = qi_client.Configuration()

# Add the API Key provided by QI
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'

# Uncomment to set up a proxy
# configuration.proxy = 'http://localhost:3128'

# create an instance of the API class
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))

#################################################################################################################
#                                                      Functions
#################################################################################################################
#
# This function retrieves a model's historical factor sensitivity data for a given period of time, a given factor
# and a given model term. 
def get_sensitivities(model, factors, start, end, term):

    # Note that this may be more than 1 year of data, so need to split requests
    year_start = int(start[:4])
    year_end = int(end[:4])
    time_series_sensitivities = {}
    
    for year in range(year_start, year_end + 1):
        query_start = start
        
        if year != year_start:
            date_from = '%d-01-01' % year
        else:
            date_from = start
            
        if year != year_end:
            date_to = '%d-12-31' % year
        else:
            date_to = end
            
        print("Gathering data for %s from %s to %s..." % (model,
                                                          date_from,
                                                          date_to))
        
        time_series_sensitivities.update(
        api_instance.get_model_sensitivities(
            model,
            date_from=date_from,
            date_to=date_to,
            term=term
            )
        )
    
    dates = []
    factor_results = {}
    # Intialize factor lists for results
    
    for factor in factors:
        factor_results[factor] = []
        
    # Iterate over each time series result
    for date in sorted(time_series_sensitivities.keys()):
        # Use the real date for the index
        dates.append(datetime.strptime(date, '%Y-%m-%d'))
        
        # This will be the sensitivities for this particular day
        daily_sensitivities = time_series_sensitivities[date]
        
        # Only consider factors requested
        for factor in factors:
            factor_result = [sensitivity['sensitivity']
                             for sensitivity in daily_sensitivities
                             if sensitivity['driver_short_name'] == factor]
            
            if len(factor_result) > 0:
                factor_results[factor].append(factor_result[0])
                
            else:
                # Pyplot will ignore nan values rather than shift datapoint left
                factor_results[factor].append(float('nan'))
                
    
    # Add date range for X axis first
    dataframe_columns = {
        'Dates': dates
    }
    
    # Add factor specific columns
    for factor in factors:
        dataframe_columns[factor] = factor_results[factor]
    
    # Initialize dataframe
    df = pandas.DataFrame(dataframe_columns)
    df.set_index('Dates', inplace=True)
    
    return df

# This function calls get_sensitivities() function to retrieve 1y1y Rate Diff., 2y2y Rate Diff. and 5y5y Rate
# Diff. long term sensitivities for USDJPY, between 2018-01-01 and 2019-01-10. 
def example_historical_factor_sensitivities():
    
    import matplotlib.pyplot as plt
    
    # To retrieve the historical sensitivities of any other model, factors, period of time or model term, change
    # the inputs of get_sensitivities() function. 
    df = get_sensitivities('USDJPY',
                           [
                               '1y1y Rate Diff.',
                               '2y2y Rate Diff.',
                               '5y5y Rate Diff.',
                            ],
                           '2015-01-01',
                           '2019-01-10',
                           'Long Term')
    
    
    fig = plt.figure(figsize=(18, 6))
    
    ax = plt.subplot(111)
    fig.patch.set_facecolor('#FFFFFF')
    
    plt.plot(df.index.values, df['1y1y Rate Diff.'], label='1y1y Rate Diff')
    plt.plot(df.index.values, df['2y2y Rate Diff.'], label='2y2y Rate Diff')
    plt.plot(df.index.values, df['5y5y Rate Diff.'], label='5y5y Rate Diff')
    
    plt.legend(loc='upper right', prop={'size': 16})
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    plt.ylabel("Sensitivity %", fontsize=18)
    plt.xlabel('Date', fontsize=18)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    plt.title('USDJPY LT', fontsize=20)
    
    ax.axhline(0, lw=1, linestyle='--', color='k')
    
    plt.show()
    
    fig.savefig('Factor_Sensitivity_Output_USDJPY',
                bbox_inches="tight",
                facecolor=fig.get_facecolor())
    
#################################################################################################################
#                                                           Main Code
#################################################################################################################

example_historical_factor_sensitivities()
```

## Output

Tracking USDJPY’s sensitivity to interest rate differentials across different tenors. Notice that for most of 2017, FX
was highly sensitive to changes in interest rates. Since the start of 2018 however, this relationship has deteriorated,
and spot FX is currently indifferent to interest rate differentials.

![alt text](https://github.com/Quant-Insight/API_Starter_Kit/blob/master/Code_Examples/img/Factor_Sensitivity_Output_USDJPY.png "Historical Factor Sensitivities")
