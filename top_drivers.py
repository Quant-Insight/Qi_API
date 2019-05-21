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
