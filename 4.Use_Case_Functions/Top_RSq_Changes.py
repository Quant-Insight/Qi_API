def Top_RSq_Changes(models, number):

    from datetime import datetime, timedelta
    import pandas

    date_datetime = datetime.now().date() - timedelta(days=1)
    date_1m_datetime = datetime.now().date() - timedelta(days=30)
    
    date = datetime.strftime(date_datetime,'%Y-%m-%d')
    date_1m = datetime.strftime(date_1m_datetime,'%Y-%m-%d')

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
