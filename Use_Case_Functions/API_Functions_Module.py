#######################################################################################################################################
# 
# This module allows you to call all Qi use-case functions. 
#
#
# Download this script and save in your working directory. 
# Set your API Key as an environment variable.
# Import API_Functions_Module
#
#
# For Jupyter Notebooks use (API Key needs to be declared without ''):
#
#         %set_env QI_API_KEY = YOUR_API_KEY
#         import API_Functions_Module
#
#
# For other Python development environments (API Key needs to be declared as a string ''):
#
#         import os
#         import subprocess
#         import sys
#
#         os.environ['QI_API_KEY'] = 'YOUR_API_KEY'
#
#         import API_Functions 
#
#######################################################################################################################################



from __future__ import print_function 
import time
import qi_client
from qi_client.rest import ApiException
from pprint import pprint
import os
import pandas
from datetime import datetime



QI_API_KEY= os.environ.get('QI_API_KEY', None)
if not QI_API_KEY:
    print("Mandatory environment variable QI_API_KEY not set!")


configuration = qi_client.Configuration()
configuration.api_key['X-API-KEY'] = QI_API_KEY
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))



def get_top_drivers(model,number,date,term):

    
    
    sensitivity = api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)
    date = [x for x in sensitivity][0]
    df_sensitivities = pandas.DataFrame()
 
    for data in sensitivity[date]:
        df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

    top_names = abs(df_sensitivities.T).nlargest(number,0).index
    top = df_sensitivities[top_names]
    top = top.T.rename(columns={0:model})
    
    return top


def get_factor_drivers(model,date,term):

    sensitivity = api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)
    date = [x for x in sensitivity][0]
    df_sensitivities = pandas.DataFrame()
 
    for data in sensitivity[date]:
        df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

    df_sensitivities = df_sensitivities.T
    df_sensitivities = df_sensitivities.rename(columns={0:model})
    
    
    return df_sensitivities



def get_bucket_drivers(model,date,term):
    
    sensitivity = api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)

    df_sensitivities = pandas.DataFrame()
    date = [x for x in sensitivity.keys()][0]

    for data in sensitivity[date]:

        if data['bucket_name'] in df_sensitivities.columns:
            df_sensitivities[str(data['bucket_name'])][0] = df_sensitivities[str(data['bucket_name'])][0] + [data['sensitivity']]

        else:
            df_sensitivities[str(data['bucket_name'])]=[data['sensitivity']]
            
    df_sensitivities.index = ['Sensitivity']

    return df_sensitivities




def get_portfolio_sens_exposures_bucket(portfolio,date):

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




def get_portfolio_cash_exposures_bucket(portfolio,date):

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




from retrying import retry


@retry(wait_exponential_multiplier=1000,
       wait_exponential_max=10000,
       stop_max_attempt_number=100)

def get_bucket_grid(model,start,end,term):
    
    year_start = int(start[:4])
    year_end = int(end[:4])
    sensitivity = {}

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

        sensitivity.update(
        api_instance.get_model_sensitivities(
        model,
        date_from=date_from,
        date_to=date_to,
        term=term
        )
        )
    
    
    sensitivity_grid = pandas.DataFrame()
    
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:

            if data['bucket_name'] in df_sensitivities.columns:
                df_sensitivities[str(data['bucket_name'])][0] = df_sensitivities[str(data['bucket_name'])][0] + [data['sensitivity']]

            else:
                df_sensitivities[str(data['bucket_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = sensitivity_grid.append(df_sensitivities)
            

    return sensitivity_grid





def get_sensitivity_grid(model,start,end,term):
    
    
    year_start = int(start[:4])
    year_end = int(end[:4])
    sensitivity = {}
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
    
        sensitivity.update(
        api_instance.get_model_sensitivities(model=model,date_from=date_from,date_to=date_to,term=term))


    #sensitivity = api_instance.get_model_sensitivities(model=model,date_from=start_date,date_to=end_date,term=term)
    
    
    df_sensitivities = pandas.DataFrame()
    sensitivity_grid = pandas.DataFrame()
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:
            df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = sensitivity_grid.append(df_sensitivities)

            
    return sensitivity_grid



def get_sensitivities_to_factor_s(model, factors, start, end, term):
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
    dataframe_columns = {'Dates': dates}
# Add factor specific columns
    for factor in factors:
        dataframe_columns[factor] = factor_results[factor]
        # Initialize dataframe
        
    df = pandas.DataFrame(dataframe_columns)
    df.set_index('Dates', inplace=True)
    return df




def get_Rsq(model, start, end, term):
# Note that this may be more than 1 year of data, so need to split requests
    year_start = int(start[:4])
    year_end = int(end[:4])
    time_series = []
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
       
        time_series += api_instance.get_model_timeseries(
        model,
        date_from=date_from,
        date_to=date_to,
        term=term)
        
    rsq = [data.rsquare for data in time_series]
    dates = [data._date for data in time_series]
    df = pandas.DataFrame({'Dates': dates, 'Rsq': rsq})
    df.set_index('Dates', inplace=True)
    
    return df




def get_model_data(model,start,end,term):
    
    
    year_start = int(start[:4])
    year_end = int(end[:4])
    time_series = []
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
    
        time_series += api_instance.get_model_timeseries(model=model,date_from=date_from,date_to=date_to,term=term)
    
    # time_series = api_instance.get_model_timeseries(model=model,date_from=start_date,date_to=end_date,term=term)

    FVG = [data.sigma for data in time_series]
    Rsq = [data.rsquare for data in time_series]
    dates = [data._date for data in time_series]
    
    model_value = [data.fair_value for data in time_series]
    percentage_gap = [data.percentage_gap for data in time_series]
    absolute_gap = [data.absolute_gap for data in time_series]


    df_ = pandas.DataFrame({'FVG':FVG, 'Rsq':Rsq, 'Model Value':model_value, 'Percentage Gap':percentage_gap,
                            'Absolute Gap':absolute_gap})
    df_.index = dates
    
    return df_




def get_portfolio(factor,size,date,term):

    FACTOR_sensitivity = []
    names = []
    POSITION = []

    # Get ID's of the Euro Stoxx 600 Stocks.
    # Stocks can be changed by specifying another stock's tag. 
    euro_stoxx_600 = [x.name for x in api_instance.get_models(tags="STOXX Europe 600")][::20]

    for asset in euro_stoxx_600:

        sensitivity = api_instance.get_model_sensitivities(model=asset,date_from=date,date_to=date,term = term)

        df_sensitivities = pandas.DataFrame()

        if len(sensitivity) > 0:
            date = [x for x in sensitivity][0]

            for data in sensitivity[date]:
                df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]

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




def get_factor_stdevs(model,date,term):
    
# model = 'AAPL'
# date = '2019-04-26'
# term = 'Long Term'

    sensitivity = api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)
    date = [x for x in sensitivity][0]
    df_sensitivities = pandas.DataFrame()

    for data in sensitivity[date]:
        value = data['driver_zscore_window_stdev']
        df_sensitivities[str(data['driver_short_name'])]=[value]

    df_sensitivities = df_sensitivities.transpose()
    top10_names = abs(df_sensitivities).nlargest(40,0).index
    top10 = df_sensitivities.loc[top10_names]
    top10 = top10.rename(columns={0:model})
            
    return top10


