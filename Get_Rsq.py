def get_Rsq(model,start,end,term):

    time_series = api_instance.get_model_timeseries(model=model, date_from=start, date_to=end,term=term)
        
    Rsq = [data.rsquare for data in time_series]
    dates = [data._date for data in time_series]

    df = pandas.DataFrame({'Dates':dates,'Rsq':Rsq})    
    df.set_index('Dates',inplace=True)

    return(df)
