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
#                             | Name   | RSq      | RSq - 1M | Change    |
#                      | 521  | SOF    | 17.34892 | 75.72115 | -58.37223 | 
#                      | 563  | TGS    | 20.27641 | 67.37992 | -47.10351 |
#                      | 44   | ANDR   | 11.02797 | 55.16754 | -44.13957 |
#                      | 477  | SAABB  | 8.23728  | 52.26702 | -44.02974 |
#                      | 201  | EQNR   | 46.34978 | 84.55396 | -38.20418 | 
#                      | 205  | ETL    | 29.15634 | 66.03383 | -36.87749 |
#                      | 456  | REP    | 41.28672 | 77.06586 | -35.77914 |
#                      | 595  | UTDI   | 7.71155  | 43.11031 | -35.39876 |
#                      | 261  | HAS    | 80.33647 | 45.12447 | 35.21200  | 
#                      | 287  | ICA    | 13.54304 | 45.96248 | -32.41944 |
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
