#####################################################################
#
# NOTE: This will only work for Equities.
#####################################################################


def get_bucket_grid_major_bucket_groups(model,start,end,term):
    
    buckets_major_groups = {'Global Growth': 'Economic Fundamentals', 'Inf. Expec.': 'Economic Fundamentals', 'Metals': 'Economic Fundamentals',
                       'Energy': 'Economic Fundamentals', 'Corp Credit': 'Financial Conditions', 'Real Rates': 'Financial Conditions',
                       'Global QE': 'Financial Conditions', 'Country Growth': 'Financial Conditions', 'DM FX': 'Financial Conditions', 
                       'EM FX': 'Financial Conditions', 'Systemic liquidity': 'Financial Conditions', 'Risk Aversion': 'Risk Appetite',
                       'Country CDS': 'Risk Appetite', 'EM Sov Risk': 'Risk Appetite', 'Peripheral EU Sov Risk': 'Risk Appetite',
                       'Est. Earnings': 'Micro'}
    
    sensitivity = api_instance.get_model_sensitivities(model=model,date_from=start,date_to=end,term=term)
    
    sensitivity_grid = pandas.DataFrame()
    
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:
            #print('data[bucket_name] ' + str(data['bucket_name']))
            
            if data['bucket_name'] in buckets_major_groups: 
                global_bucket_name = buckets_major_groups[data['bucket_name']]
                
                if global_bucket_name in df_sensitivities.columns:
                    df_sensitivities[global_bucket_name][0] = df_sensitivities[global_bucket_name][0] + [data['sensitivity']]
                else: 
                    df_sensitivities[global_bucket_name]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        df_sensitivities = df_sensitivities[['Economic Fundamentals', 'Financial Conditions', 'Risk Appetite', 'Micro']]
        
        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = sensitivity_grid.append(df_sensitivities)

    return sensitivity_grid


def get_Rsq(model,start,end,term):

    time_series = api_instance.get_model_timeseries(model=model, date_from=start, date_to=end,term=term)
        
    Rsq = [data.rsquare for data in time_series]
    dates = [data._date for data in time_series]

    df = pandas.DataFrame({'Dates':dates,'Rsq':Rsq})    
    df.set_index('Dates',inplace=True)

    return(df)
