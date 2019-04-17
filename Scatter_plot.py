def scatter_plot(dataTable):

    import plotly.plotly as py
    import plotly.graph_objs as go

    import numpy as np
    
    #dataTable = dataTable[dataTable['Rsq']>65]
    #dataTable = dataTable[abs(dataTable['Infl. Expec. Sensitivity'])>0.25]

    buy_table = dataTable[dataTable['FVG']<0]
    buy_pos_table = buy_table[buy_table['Infl. Expec. Sensitivity']>0]
    buy_neg_table = buy_table[buy_table['Infl. Expec. Sensitivity']<0]
    
    sell_table = dataTable[dataTable['FVG']>0]
    sell_pos_table = sell_table[sell_table['Infl. Expec. Sensitivity']>0]
    sell_neg_table = sell_table[sell_table['Infl. Expec. Sensitivity']<0]

    buy_pos_Name = buy_pos_table['Name'].tolist()
    buy_pos_FVG = buy_pos_table['FVG']
    buy_pos_Rsq = buy_pos_table['Rsq']
    #buy_pos_sensitivities = [1/(abs(x)**3.1) for x in buy_pos_table.iloc[:,1]]
    buy_pos_sensitivities = [1/(abs(x)**1.5) for x in buy_pos_table.iloc[:,1]]
    
    sell_pos_Name = sell_pos_table['Name'].tolist()
    sell_pos_FVG = sell_pos_table['FVG']
    sell_pos_Rsq = sell_pos_table['Rsq']
    #sell_pos_sensitivities = [1/(abs(x)**3.1) for x in sell_pos_table.iloc[:,1]]
    sell_pos_sensitivities = [1/(abs(x)**1.5) for x in sell_pos_table.iloc[:,1]]
    
    buy_neg_Name = buy_neg_table['Name'].tolist()
    buy_neg_FVG = buy_neg_table['FVG']
    buy_neg_Rsq = buy_neg_table['Rsq']
    #buy_neg_sensitivities = [1/(abs(x)**3.1) for x in buy_neg_table.iloc[:,1]]
    buy_neg_sensitivities = [1/(abs(x)**1.5) for x in buy_neg_table.iloc[:,1]]

    sell_neg_Name = sell_neg_table['Name'].tolist()
    sell_neg_FVG = sell_neg_table['FVG']
    sell_neg_Rsq = sell_neg_table['Rsq']
    #sell_neg_sensitivities = [1/(abs(x)**3.1) for x in sell_neg_table.iloc[:,1]]
    sell_neg_sensitivities = [1/(abs(x)**1.5) for x in sell_neg_table.iloc[:,1]]


    trace0 = go.Scatter(
        x = buy_pos_Rsq,
        y = buy_pos_FVG,
        text = buy_pos_Name,
        mode = 'markers',
        name = 'Buy, + sensitivity',
        marker = dict(
            size = buy_pos_sensitivities,
            color = 'green',
            line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
            )

        )
    )

    trace1 = go.Scatter(
        x = sell_pos_Rsq,
        y = sell_pos_FVG,
        text = sell_pos_Name,
        name = 'Sell, + sensitivity',
        mode = 'markers',
        marker = dict(
            size = sell_pos_sensitivities,
            color = 'red',
            line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
            )

        )
    )
    
    
    trace2 = go.Scatter(
        x = buy_neg_Rsq,
        y = buy_neg_FVG,
        text = buy_neg_Name,
        mode = 'markers',
        name = 'Buy, - sensitivity',
        marker = dict(
            size = buy_neg_sensitivities,
            color = 'green',
            symbol = 'circle-open',
            line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
            )

        )
    )

    trace3 = go.Scatter(
        x = sell_neg_Rsq,
        y = sell_neg_FVG,
        text = sell_neg_Name,
        name = 'Sell, - sensitivity',
        mode = 'markers',
        marker = dict(
            size = sell_neg_sensitivities,
            color = 'red',
            symbol = 'circle-open',
            line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
            )

        )
    )

    data = [trace0, trace1, trace2, trace3]

    layout = dict(title = 'Adage Stocks Sensitivity to Infl. Expec.',
                  yaxis = dict(zeroline = True,range = [-2,5], title = 'FVG', showgrid=False),
                  xaxis = dict(zeroline = False, title = 'Rsq', showgrid=False),
                  hovermode = 'closest',
                 )

    fig = dict(data=data, layout=layout)
    return py.iplot(fig, filename='apf/Adage/Adage Stocks Sensitivity to Infl. Expec. test')



def get_sensitivities_to_bucket(stocks,bucket,date,term):
#(size)

#bucket = 'Infl. Expec.'
#date = '2019-3-11'
#term = 'Long Term'

    Bucket_sensitivity = []
    names = []
    POSITION = []
    FVG = []
    Rsq = []

    # Get ID's of the Euro Stoxx 600 Stocks
    #Euro_stoxx_600_IDs = range(4691,5891,2)

    # SPX500_stocks

    for i in stocks:

        all_buckets = get_bucket_drivers(i,date,term) 

        if all_buckets is not None:
            Bucket_sens = float(all_buckets[bucket])

            Bucket_sensitivity.append(Bucket_sens)
            names.append(i)
        #               FVG.append(float(get_vals(i,date,date,'Long Term')['FVG']))
        #               Rsq.append(float(get_vals(i,date,date,'Long Term')['Rsq']))
         #   print(spx500_stocks.index(i))

    df_bucket_sensit = pandas.DataFrame({'Name':names,bucket+' Sensitivity':Bucket_sensitivity})
    #    df_abs_factor_sensit = pandas.DataFrame({'Name':names,factor+' Sensitivity':[abs(x) for x in FACTOR_sensitivity]})
     #   stock_names = df_abs_factor_sensit.nlargest(size,str(factor)+' Sensitivity')['Name']
      #  stocks = df_factor_sensit.loc[df_factor_sensit['Name'].isin(stock_names)]

    return df_bucket_sensit

def get_bucket_drivers(model,date,term):

    try:
        sensitivity = api_instance.get_model_sensitivities(model=model,date_from=date,date_to=date,term=term)
        
        df_sensitivities = pandas.DataFrame()
    
        if len(sensitivity)>0:
            date = [x for x in sensitivity][0]

            for data in sensitivity[date]:

                if data['bucket_name'] in df_sensitivities.columns:
                    df_sensitivities[str(data['bucket_name'])][0] = df_sensitivities[str(data['bucket_name'])][0] + [data['sensitivity']]

                else:
                    df_sensitivities[str(data['bucket_name'])]=[data['sensitivity']]

            return df_sensitivities
        
    except ApiException as e:
        print("Exception when calling DefaultApi->get_instrument: %s\n" % e)
