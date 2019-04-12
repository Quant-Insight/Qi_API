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
    
        sensitivity.update(
        api_instance.get_model_sensitivities(
        model,
        date_from=date_from,
        date_to=date_to,
        term=term
        )
        )

    
    df_sensitivities = pandas.DataFrame()
    sensitivity_grid = pandas.DataFrame()
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:
            df_sensitivities[str(data['driver_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = sensitivity_grid.append(df_sensitivities)

            
    return sensitivity_grid
