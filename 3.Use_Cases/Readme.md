# Use-Case Functions

## Get Portfolio

### Description

This function creates a portfolio of European stocks based on sensitivities to a given factor. 

**#Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** 

* factor - 'factor' (e.g. 'ADXY')
* universe - universe of stocks to choose from (e.g. ['BMW','VIE','ATL'....])
* size - number of stocks to be in resulting portfolio (e.g. 10)
* date - 'date' (e.g. '2019-05-17')
* term - 'term' (e.g. 'Long Term')
               
**Output:** 
Dataframe with the following columns:

* Position - dataframe index. 
* Name - top 5 factor drivers' names. 
* Weight - weights of the top 5 factor drivers.
* Factor Sensitivity - Factor top 5 drivers' sensitivity.

### Code

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

# Get stock universe
universe = [x.name for x in api_instance.get_models(tags="STOXX Europe 600")][::2]


#################################################################################################################
#                                                      Function
#################################################################################################################
# 

def get_portfolio(factor,universe,size,date,term):

    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:
        
        FACTOR_sensitivity = []
        names = []
        POSITION = []

        for asset in universe:

            sensitivity = api_instance.get_model_sensitivities(model=asset,date_from=date,date_to=date,term = term)

            df_sensitivities = pandas.DataFrame()

            if len(sensitivity) > 0:
                date = [x for x in sensitivity][0]

                for data in sensitivity[date]:
                    df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]
                # We want the top 5 drivers in absolute terms. 
                top5 = abs(df_sensitivities).T.nlargest(5,0)
                Factor_sens = float(df_sensitivities[factor])

                if factor in top5.index:
                    FACTOR_sensitivity.append(Factor_sens)
                    names.append(asset)
                    position = top5.index.tolist().index(factor)+1
                    POSITION.append(position)

        df_factor_sensit = pandas.DataFrame({'Name':names,'Position':POSITION,factor+' Sensitivity':FACTOR_sensitivity})
        portfolio = df_factor_sensit.nlargest(size,str(factor)+' Sensitivity')

        sw = 1/(portfolio['Position']+2)
        Weights = sw/sw.sum()

        portfolio = portfolio.drop(['Position'], axis=1)
        portfolio.insert(1,'Weight',Weights)

        return portfolio
    
    
#################################################################################################################
#                                                           Main Code
#################################################################################################################

get_portfolio(factor = 'ADXY', size = 10, date = '2019-05-17', term = 'Long Term')
```

### Output

|    | Name | Weight    | ADXY Sensitivity |
|----|:----:|:---------:|:----------------:| 
| 18 | ENEL | 0.108527  | 0.12556          |
| 27 | GET  | 0.077519  | 0.12079          |
| 71 | VIE  | 0.108527  | 0.11375          |
| 67 | TEL  | 0.090439  | 0.11198          |
| 5  | ATL  | 0.108527  | 0.10966          |
| 2  | ALT  | 0.108527  | 0.10409          |
| 53 | RHM  | 0.090439  | 0.10178          |
| 1  | AENA | 0.108527  | 0.10067          |
| 62 | SGRE | 0.090439  | 0.10050          |
| 40 | LOOMB| 0.108527  | 0.09925          |


## Optimise Trade Selection

### Description

This function returns the top stocks based on sensitivities (in absolute terms) to a given list of factors.

**#Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** 

* factor - list of factors. We recommend to use a maximum of 3 factors (e.g. ['ADXY', 'US GDP', 'Brent'])
* universe_asset_classes - universe asset class (e.g. 'Equity')
* size - number of models to be in the result (e.g. 10)
* date - 'date' (e.g. '2019-05-17')
* term - 'term' (e.g. 'Long Term')
* universe_tag (optional) - universe tag (e.g. 'STOXX Europe 600') - The list of the tags can be retrieved using api_instance.get_tags()
               
**Output:** 
Dataframe with the following columns:

* Position - dataframe index. 
* Name - top 5 factor drivers' names. 
* Weight - weights of the top 5 factor drivers.
* Factor Sensitivity - Factor top 5 drivers' sensitivity.

### Code

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
#                                                      Function
#################################################################################################################
# 
def optimise_trade_selection(factors,universe_asset_classes,size,date,term, **kwargs):
    
    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:
        
        FACTOR_sensitivity = []
        names = []
        POSITION = []

        universe_tag = kwargs.get('universe_tag', None)

        if len(factors) > 3:
            print('The number of factors need to be less than 3.')
        else:   

            if (universe_tag is not None):
                models = [x.name for x in api_instance.get_models(asset_classes = universe_asset_classes, tags=universe_tag)][::2]
            else:
                models = [x.name for x in api_instance.get_models(asset_classes = universe_asset_classes)][::2]

            df_result = pandas.DataFrame(columns = factors + ['Total Sensitivity (Abs)'])

            print('Gathering data for all the models in the universe (it can take a while depending on the universe chosen)')

            for asset in models:
                factor_sensitivities = []
                sensitivity = api_instance.get_model_sensitivities(model=asset,date_from=date,date_to=date,term = term)

                df_sensitivities = pandas.DataFrame()

                if len(sensitivity) > 0:
                    date = [x for x in sensitivity][0]

                    for data in sensitivity[date]:
                        df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]


                    total = 0
                    for factor in factors:
                        total += abs(df_sensitivities[factor][0])
                        factor_sensitivities.append(df_sensitivities[factor][0])

                    df_result.loc[asset] = factor_sensitivities + [total]

            if len(df_result) > 0:
                result = df_result.nlargest(size,'Total Sensitivity (Abs)')
                return result
            else:
                if universe_tag is not None:
                    print('There are no models which satisfies the universe asset classes ' + universe_asset_classes + ' and the universe tag ' + universe_tag)
                else:
                    print('There are no models which satisfies the universe asset classes ' + universe_asset_classes)
    
    
#################################################################################################################
#                                                           Main Code
#################################################################################################################

optimise_trade_selection(factors = ['ADXY', 'US GDP', 'Brent'], universe_asset_classes = 'Equity', size = 10, date = '2019-05-17', term = 'Long Term', universe_tag = 'STOXX Europe 600')
```

### Output

|Name |	ADXY     | US GDP   | Brent | Total Sensitivity |
|:---:|:--------:|:--------:|:-----------:|:-----------:|
|AGS  | -0.09107 | -0.00024 | 0.22146     | 0.31277     |
|ASRNL|	-0.11486 | -0.00086 | 0.19477     | 0.31049     |
|STB  |	-0.10449 | -0.00068 | 0.20225     | 0.30742     |
|ETL  |	-0.15895 | -0.00156 | 0.14606     | 0.30657     |
|BC8  |	-0.10468 | -0.00068 | 0.19653     | 0.30189     |
|SAABB|	-0.14782 | -0.00172 | 0.15073     | 0.30027     |
|UPM  |	-0.08579 | -0.00010 | 0.21040     | 0.29629     |
|FPE3 |	-0.11327 | -0.00138 | 0.18078     | 0.29543     |
|ENEL |	0.12556  | 0.00070  | -0.16881    | 0.29507     |
|GALE |	-0.08880 | -0.00004 | 0.19907     | 0.28791     |



## Portfolio % Exposures

### Description

This function creates a table with the sensitivities weight exposures in % of a given portfolio on a bucket level, for a given period of time for each stock in the portfolio. It also provides the portfolio total sensitivities weight exposures per bucket.

**#Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** 

* portfolio - model (e.g. 'AAPL')

The portfolio has to be in the following format:

portfolio = pandas.DataFrame({'Name':[stock a, stock b, stock c],
                              'Weight':[0.3, 0.3, 0.4],
                              'L/S':[1,-1,1]})

stock a, b and c must be names of models in the Qi API, e.g. AAPL, MSFT, FB

This can be done by manually inputting the data (as seen above), or by importing an Excel file, or csv file like so:

    xl = pandas.ExcelFile('file_location/file_name')
    portfolio = xl.parse('Sheet_name')

    OR

    portfolio = pandas.read_csv('file_location/file_name')

    The three inputs that need updating here are: file_location, file_name and Sheet_name

    The Excel/csv file must be in the following format:

    | Name | Weight  | L/S |
    | AAPL |   0.3   |  1  |
    | MSFT |   0.3   | -1  |
    | FB   |   0.4   |  1  |

* date - portfolio date (e.g. '2019-05-20') 
               
**Output:** 
Dataframe with the following columns:

* Column with all the portfolio stock names plus the 'Total' row - dataframe index. 
* A column per Bucket with its weight sensitivities in % associated to each stock in the portfolio. 

### Code

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
#                                                      Function
#################################################################################################################
# 
def get_portfolio_sens_exposures_bucket(portfolio,date):
    
    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:

        stock_names = portfolio['Name']
        df_tot = pandas.DataFrame()

        for stock in stock_names:

            sensitivity = api_instance.get_model_sensitivities(model=stock,date_from=date,date_to=date,term='Long Term')
            df_sensitivities = pandas.DataFrame()
            date = [x for x in sensitivity.keys()][0]


            for data in sensitivity[date]:

                if data['bucket_name'] in df_sensitivities.columns:
                    df_sensitivities[str(data['bucket_name'])][0] = df_sensitivities[str(data['bucket_name'])][0] + [data['sensitivity']]

                else:
                    df_sensitivities[str(data['bucket_name'])]=[data['sensitivity']]

            df_sensitivities = df_sensitivities.rename(index={0:stock})
            df_sensitivities = df_sensitivities.sort_index(axis=1)
            if df_tot.empty:
                df_tot = df_sensitivities
            else:
                df_tot = df_tot.append(df_sensitivities)


        portfolio_sensitivities = pandas.DataFrame({},columns = df_tot.columns)

        for stock in stock_names:

            portfolio_sensitivities.loc[stock] = [a*float(portfolio[portfolio['Name']==stock]['Weight'])*float(portfolio[portfolio['Name']==stock]['L/S']) for a in df_tot.loc[stock]]

        portfolio_sensitivities.loc['Total'] = [portfolio_sensitivities[x].sum() for x in portfolio_sensitivities.columns]

        portfolio_exposures = portfolio_sensitivities.loc[['Total']]

        return portfolio_sensitivities

    
#################################################################################################################
#                                                           Main Code
#################################################################################################################

portfolio = pandas.DataFrame({'Name':['AAPL', 'MSFT', 'FB'],
                              'Weight':[0.3, 0.3, 0.4],
                              'L/S':[1,-1,1]})
date = '2019-05-20'

get_portfolio_sens_exposures_bucket(portfolio,date)
```

### Output

|       | Corp credit | DM FX     | EM FX     | EM Sov Risk | Energy    | Est. Earnings | ... |
|:-----:|:-----------:|:---------:|:---------:|:-----------:|:---------:|:-------------:|:---:|
| AAPL  | -0.062982   | -0.001827 | -0.022824 | 0.010242    | 0.046779  | 0.032241      | ... |
| MSFT  | 0.037995    | -0.000489 | 0.002154  | 0.006750    | -0.018942 | -0.000282     | ... |
| FB    | 0.107824    |  0.019104 | 0.022536  | 0.015764    | -0.006672 | 0.083188      | ... |
| Total | 0.082837    |  0.016788 | 0.001866  | 0.032756    |  0.021165 | 0.115147      | ... |



## Portfolio Cash Exposures

### Description

This function creates a table with the cash exposures of a given portfolio on a bucket level, for a given period of time for each stock in the portfolio. It also provides the portfolio total cash exposures per bucket.

**#Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** 

* portfolio - model (e.g. 'AAPL')

The portfolio has to be in the following format:

portfolio = pandas.DataFrame({'Name':[stock a, stock b, stock c],
                            'Position':[1000000, -1000000, 1000000]})

stock a, b and c must be names of models in the Qi API, e.g. AAPL, MSFT, FB

This can be done by manually inputting the data (as seen above), or by importing an Excel file, or csv file like so:

    xl = pandas.ExcelFile('file_location/file_name')
    portfolio = xl.parse('Sheet_name')

    OR

    portfolio = pandas.read_csv('file_location/file_name')

    The three inputs that need updating here are: file_location, file_name and Sheet_name

    The Excel/csv file must be in the following format:

    | Name | Position |
    | AAPL | 1000000  |
    | MSFT | -1000000 |
    | FB   | 1000000  |

* date - portfolio date (e.g. '2019-05-20') 
               
**Output:** 
Dataframe with the following columns:

* Column with all the portfolio stock names plus the 'Total' row - dataframe index.
* A column per Bucket with its chash sensitivities associated to each stock in the portfolio.

### Code

```python
def get_portfolio_cash_exposures_bucket(portfolio,date):    
    
    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:

        stock_names = portfolio['Name']
        df_tot = pandas.DataFrame()

        for stock in stock_names:

            sensitivity = api_instance.get_model_sensitivities(model=stock,date_from=date,date_to=date,term='Long Term')
            df_sensitivities = pandas.DataFrame()
            date = [x for x in sensitivity.keys()][0]

            for data in sensitivity[date]:

                if data['bucket_name'] in df_sensitivities.columns:
                    df_sensitivities[str(data['bucket_name'])][0] = df_sensitivities[str(data['bucket_name'])][0] + [data['sensitivity']]

                else:
                    df_sensitivities[str(data['bucket_name'])]=[data['sensitivity']]

            df_sensitivities = df_sensitivities.rename(index={0:stock})
            df_sensitivities = df_sensitivities.sort_index(axis=1)
            if df_tot.empty:
                df_tot = df_sensitivities
            else:
                df_tot = df_tot.append(df_sensitivities)


        portfolio_sensitivities = pandas.DataFrame({},columns = df_tot.columns)

        for stock in stock_names:

            portfolio_sensitivities.loc[stock] = [a*float(portfolio[portfolio['Name']==stock]['Position'])/100 for a in df_tot.loc[stock]]

        portfolio_sensitivities.loc['Total'] = [portfolio_sensitivities[x].sum() for x in portfolio_sensitivities.columns]

        portfolio_exposures = portfolio_sensitivities.loc[['Total']]

        return portfolio_sensitivities

#################################################################################################################
#                                                  Main Code
#################################################################################################################

portfolio = pandas.DataFrame({'Name':['AAPL', 'MSFT', 'FB'],
                              'Position':[1000000, -1000000, 1000000]})
date = '2019-05-20'

get_portfolio_cash_exposures_bucket(portfolio,date)
```

### Output

|            | Corp credit | DM FX | EM FX  | EM Sov Risk | Energy | Est. Earnings | ... |
|:----------:|:-----------:|:-----:|:------:|:-----------:|:------:|:-------------:|:---:|
| AAPL       | -2099.4     | -60.9 | -760.8 | 341.4       | 1559.3 | 1074.7        | ... |
| MSFT       | 1266.5      | -16.3 | 71.8   | 225.0       | -631.4 | -9.4          | ... |
| FB         | 2695.6      | 477.6 | 563.4  | 394.1       | -166.8 | 2079.7        | ... |
| Total      | 1862.7      | 400.4 | -125.6 | 960.5       | 761.1  | 3145.0        | ... |


## Scenario Analysis

### Description

This function creates a table showing the % change of an asset due to various combinations of movements in two factors.

**#Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** 

* model - model ticker (e.g. 'AAPL')
* factors - 2 factors you want to compare (e.g. ['Brent', 'Copper']) 
* date - date (e.g. '2019-05-17')
* term - term (e.g. 'Long Term')
               
**Output:** 

* Dataframe representing the % change of an asset as a result of certain movements in two factors.
### Code

```python

def get_sens_matrix(model,factors,date,term):    
    
    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:

        drivers = get_factor_drivers(model,date,term)

        stdevs = get_factor_stdevs(model,date,term)

        both_moves = []
        both_results = []
        for factor in factors:

            if float(stdevs.loc[factor]) > 5:
                move_c = int(round(float(stdevs.loc[factor]),-1))
                intervals = int(round(move_c/2,0))
                moves = range(move_c - (intervals*5),move_c + (intervals*2),intervals)

            elif float(stdevs.loc[factor]) > 2:
                move_c = int(round(float(stdevs.loc[factor]),0))
                intervals = int(round(move_c/2,0))
                moves = range(move_c - (intervals*5),move_c + (intervals*2),intervals)

            elif float(stdevs.loc[factor]) < 0.05:
                move_c = round(float(stdevs.loc[factor]),2)
                intervals = int((move_c/2)*100)
                move_c = int(100*move_c)
                moves = range(move_c - (intervals*5),move_c + (intervals*2),intervals)
                moves = [round(x/100,2) for x in moves]

            else:
                move_c = round(float(stdevs.loc[factor]),1)
                intervals = int((move_c/2)*100)
                move_c = int(100*move_c)
                moves = range(move_c - (intervals*5),move_c + (intervals*2),intervals)

                if intervals < 10:
                    moves = [round(x/100,2) for x in moves]

                else:
                    moves = [round(x/100,1) for x in moves]

            both_moves.append(moves)
            sens = float(drivers.loc[factor])
            stdev = float(stdevs.loc[factor])
            move_results = [(move/stdev)*sens for move in moves]
            both_results.append(move_results)

        total_moves = []
        for x in both_results[0]:
            total_moves.append([x+y for y in both_results[1]])

        final_df = pandas.DataFrame(total_moves, columns=both_moves[1], index=both_moves[0])
        final_df = round(final_df,2)

        return final_df

#################################################################################################################
#                                                  Main Code
#################################################################################################################

get_sens_matrix(model = 'AAPL', factors = ['Brent', 'Copper'], date  = '2019-05-17', term = 'Long Term')

```

### Output


|     | -15   |	-10   | -5    | 0     | 5     | 10    | 15    |
|:---:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| -15 |	-0.22 |	-0.25 | -0.27 | -0.29 | -0.31 | -0.34 | -0.36 | 
| -10 |	-0.13 |	-0.15 | -0.17 | -0.19 | -0.22 | -0.24 | -0.26 | 
| -5  |	-0.03 | -0.05 | -0.07 | -0.10 | -0.12 | -0.14 | -0.16 |
| 0   | 0.07  | 0.04  | 0.02  | 0.00  | -0.02 | -0.04 | -0.07 |
| 5   | 0.16  | 0.14  | 0.12  | 0.10  | 0.07  | 0.05  | 0.03  | 
| 10  | 0.26  | 0.24  | 0.22  | 0.19  | 0.17  | 0.15  | 0.13  | 
| 15  | 0.36  | 0.34  | 0.31  | 0.29  | 0.27  | 0.25  | 0.22  |


## Top RSq

### Description

This function creates a table with the top RSq changes of a given list of models. 

**#Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** 

* models - list of models (e.g. ['AAPL', 'FB', 'MSFT'])
* number - number of results to be shown in the result (e.g. 10) 

               
**Output:** 
Dataframe with the following columns:

* Name: name of the top models. 
* RSq: RSq most recent values (yesterday's values) for each of the top models.
* RSq - 1M: RSq values (from a month before) for each of the top models. 
* Change: Change between the RSq values obtained.   

### Code

```python

def Top_RSq_Changes(models, number):

    from datetime import datetime, timedelta
    import pandas
    
    # Data is just available from Monday to Friday. We need to check that the dates we are choosing are between those days. 
    if datetime.today().weekday() == 0:
        date = datetime.strftime(datetime.now() - timedelta(3), '%Y-%m-%d')
    elif datetime.today().weekday() == 6:
        date = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')
    else:
        date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    
    date_1m_datetime = datetime.now().date() - timedelta(days=30)
    
    if date_1m_datetime.weekday() == 0:
        date_1m = datetime.strftime(date_1m_datetime - timedelta(3), '%Y-%m-%d')
    elif date_1m_datetime.weekday() == 6:
        date_1m = datetime.strftime(date_1m_datetime - timedelta(2), '%Y-%m-%d')
    else:
        date_1m = datetime.strftime(date_1m_datetime - timedelta(1), '%Y-%m-%d')
        

    Rsq_s = []
    Rsq_1m = []
    asset_names = []

    for asset in models:

        rsq_now = get_rsq(asset,date,date,'Long Term')
        rsq_past = get_rsq(asset,date_1m,date_1m,'Long Term')

        if (len(rsq_now) > 0) and (len(rsq_past) > 0):
            
            Rsq_s.append(float(rsq_now['Rsq']))
            Rsq_1m.append(float(rsq_past['Rsq']))
            
            name = api_instance.get_model(asset).security_name
            asset_names.append(asset)

        
    df_RSq = pandas.DataFrame({'Name':asset_names,'RSq':Rsq_s,'RSq - 1M':Rsq_1m,
                               'Change':[x-y for x,y in zip(Rsq_s,Rsq_1m)]})
    
    df_top_RSq = df_RSq.loc[abs(df_RSq['Change']).nlargest(number).index]
    
    return df_top_RSq


#################################################################################################################
#                                                  Main Code
#################################################################################################################

models = [x.name for x in api_instance.get_models(tags="STOXX Europe 600")][::2]

Top_RSq_Changes(models = models, number = 10)

```

### Output



|      | Name   | RSq      | RSq - 1M   | Change    |
|:----:|:------:|:--------:|:----------:|:---------:|
| 388  | ORK    | 76.16359 | 21.26871   | 54.89488  |
| 201  | EZJ    | 13.07574 | 61.41113   | -48.33539 |
| 406  | PPB    | 4.23548  | 52.08732   | -47.85184 |
| 93   | BNZL   | 46.49451 | 2.33265    | 44.16186  | 
| 260  | HNR1   | 30.91065 | 73.36905   | -42.45840 |
| 589  | YAR    | 23.98230 | 63.99933   | -40.01703 | 
| 561  | UTDI   | 70.68089 | 32.27736   | 38.40353  | 
| 307  | KESKOB | 0.31400  | 38.03919   | -37.72519 |
| 190  | EPIA   | 60.45243 | 24.29324   | 36.15919  |
| 416  | PUM    | 40.85825 | 75.93390   | -35.07565 |


