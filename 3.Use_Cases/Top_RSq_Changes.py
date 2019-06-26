#######################################################################################################################################
# 
# This function creates a table with the top RSq changes of a given list of models.
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         models - list of models (e.g. ['AAPL', 'FB', 'MSFT'])
#         number - number of results to be shown in the result (e.g. 10)
#
# Output: 
#         dataframe with the following columns:
#               * Name: name of the top models.
#               * RSq: RSq most recent values (yesterday's values) for each of the top models.
#               * RSq - 1M: RSq values (from a month before) for each of the top models.
#               * Change: Change between the RSq values obtained.
#               * e.g.
#                      |      | Name   | RSq      | RSq - 1M  | Change    | 
#                      | 388  | ORK    | 76.16359 | 21.26871  | 54.89488  | 
#                      | 201  | EZJ    | 13.07574 | 61.41113  | -48.33539 |
#                      | 406  | PPB    | 4.23548  | 52.08732  | -47.85184 | 
#                      | 93   | BNZL   | 46.49451 | 2.33265   | 44.16186  | 
#                      | 260  | HNR1   | 30.91065 | 73.36905  | -42.45840 | 
#                      | 589  | YAR    | 23.98230 | 63.99933  | -40.01703 | 
#                      | 561  | UTDI   | 70.68089 | 32.27736  | 38.40353  | 
#                      | 307  | KESKOB | 0.31400  | 38.03919  | -37.72519 | 
#                      | 190  | EPIA   | 60.45243 | 24.29324  | 36.15919  | 
#                      | 416  | PUM    | 40.85825 | 75.93390  | -35.07565 | 
#
#######################################################################################################################################


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
