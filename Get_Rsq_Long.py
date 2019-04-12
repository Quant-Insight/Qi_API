def get_rsq_long(model, start, end, term):
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
