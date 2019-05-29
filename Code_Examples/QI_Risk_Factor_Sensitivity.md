## Description

This piece of code creates a csv file with a portfolio sensitive to a given factor. 

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


**Inputs:** For the purpose of this example, the models, the factor, the size of th portfolio, the funds and the date are already defined in 
example_qi_risk_factor_sensitivity() function. 
               
**Output:** A csv file with a portfolio sensitive to ADXY.
               
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
# This function creates a portfolio sensitive to a given factor. 
def get_portfolio(factor, models, size, funds, date):
    FACTOR_sensitivity = []
    names = []
    POSITION = []
    
    for model in models:
        print("Getting model sensitivities for %s on %s" % (model, date))
        sensitivity = api_instance.get_model_sensitivities(
                model=model,
                date_from=date,
                date_to=date
                )
    
    df_sensitivities = pandas.DataFrame()
    
    #if date not in sensitivity: 
    #     continue
    
    for data in sensitivity[date]:
        df_sensitivities[str(data['driver_short_name'])] = [
                data['sensitivity']
        ]
    
    top10 = df_sensitivities.transpose().nlargest(10, 0)
    
    Factor_sens = float(df_sensitivities[factor])
    
    if factor in top10.index and Factor_sens > 0:
        FACTOR_sensitivity.append(Factor_sens)
        names.append(api_instance.get_model(model=model).name)
        position = top10.index.tolist().index(factor) + 1
        POSITION.append(position)
        portfolio_size = size
        df_factor_sensit = pandas.DataFrame({
                'Name': names,
                'Position': POSITION,
                factor + ' Sensitivity': FACTOR_sensitivity
                })
    
    portfolio = df_factor_sensit.nlargest(portfolio_size,
                                          str(factor) + ' Sensitivity')
    
    sw = 1 / (portfolio['Position'] + 2)
    summ = sum(sw)
    Weights = sw/summ
    position_values = [funds*x for x in Weights]
    
    factor_exposure = [a*b/100 for a, b in zip(
            portfolio[factor + ' Sensitivity'],
            position_values)]
    
    portfolio = portfolio.drop(['Position'], axis=1)
    portfolio.insert(1, 'Weight', Weights)
    portfolio.insert(2, 'Position Value', position_values)
    portfolio[factor + ' Exposure'] = factor_exposure
    
    return portfolio

# This function creates a portfolio sensitive to ADXY.
def example_qi_risk_factor_sensitivity():
    
    stoxx_600 = list(set([
            model.name for model in api_instance.get_models(tags='STOXX Europe 600')
    ]))
    
    portfolio = get_portfolio('ADXY',
                              sorted(stoxx_600),
                              10,
                              1000000,
                              '2018-06-29')
    
    portfolio.to_csv(path_or_buf='Risk_Factor_Sensitivity.csv',
                     float_format='%.5f',
                     index=False,
                     columns=[
                             'Name',
                             'Weight',
                             'Position Value',
                             'ADXY Sensitivity',
                             'ADXY Exposure'
                     ])
    print(portfolio)   
#######################################################################################################################################
#                                                           Main Code
#######################################################################################################################################

example_qi_risk_factor_sensitivity()
```

## Output

* csv file with the Portfolio

|Name	  | Weight	  | Position Value	| ADXY Sensitivity	| ADXY Exposure |
| ----- | --------: | --------------: | ----------------: | ------------: |
|RNO	  | 0.13013 	| 130131.6809	    | 0.09682	          | 125.99349     |
|EBS	  | 0.10844	  | 108443.0674	    | 0.08991	          | 97.50116      |
|ENX	  | 0.09295	  | 92951.20062	    | 0.08434	          | 78.39504      | 
|ASM	  | 0.09295	  | 92951.20062	    | 0.08349	          | 77.60496      |
|MTRO	  | 0.09295	  | 92951.20062	    | 0.08053	          | 74.8536       |
|VACN	  | 0.13013	  | 130131.6809	    | 0.07887	          | 102.63486     |
|TIT	  | 0.10844	  | 108443.0674	    | 0.07807	          | 84.6615       |
|GLE	  | 0.10844	  | 108443.0674	    | 0.07402	          | 80.26956      |
|MB	    | 0.05422	  | 54221.53369	    | 0.07019	          | 38.05809      |
|SREN	  | 0.08133	  | 81332.30054	    | 0.07016	          | 57.06274      |
