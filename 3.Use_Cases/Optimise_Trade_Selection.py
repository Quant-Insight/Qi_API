#######################################################################################################################################
# 
# This function returns the top stocks based on sensitivities (in absolute terms) to a given list of factors. 
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         factor - list of factors. We recommend to use a maximum of 3 factors (e.g. ['China GDP', 'US GDP', 'WTI'])
#         universe_asset_classes - universe asset class (e.g. 'Equity')
#         size - number of models to be in the result (e.g. 10)
#         date - 'date' (e.g. '2022-04-04')
#         term - 'term' (e.g. 'Long Term')
#         universe_tag (optional) - universe tag (e.g. 'S&P 500') - The list of the tags can be retrieved using api_instance.get_tags()
#
# Output: 
#         dataframe with the following columns:
#               * Name - top factor drivers' names (10 for our example). 
#               * Factor Sensitivities - one column per factor with the sensitivities values. 
#               * Total Sensitivities (Abs) - Total sum of the sensitivities per model, in absolute terms. 
#               * e.g.
# 
#
#                 |         | China GDP   | US GDP   | WTI     | Total Sensitivity (Abs) |
#                 |:-------:|:-----------:|:--------:|:-------:|:-----------------------:|
#                 | PYPL    |3.76613      |2.30806   |-1.38031 |7.4545                   |
#                 | NFLX    |-3.17365     |-1.94496  |-1.15896 |6.27757                  |
#                 | CDAY    |-2.43419     |-1.49178  |-1.17453 |5.1005                   |
#                 | ETSY    |-2.27569     |-1.39465  |-0.64289 |4.31323                  |
#                 | AMD     |-2.03337     |-1.24614  |-0.65696 |3.93647                  |
#                 | PAYC    |-1.87699     |-1.15031  |-0.89898 |3.92628                  |
#                 | MRNA    |0.11548      |0.07077   |-2.9552  |3.14145                  |
#                 | GPN     |1.45564      |0.89208   |0.63261  |2.98033                  |
#                 | CRM     |-1.40891     |-0.86344  |-0.57954 |2.85189                  |
#                 | FIS     |1.46804      |0.89968   |0.45805  |2.82577                  |
#
#######################################################################################################################################


def optimise_trade_selection(factors,universe_asset_classes,size,date,term, **kwargs):
    
    date_formated = datetime.strptime(date, '%Y-%m-%d')
    
    if (date_formated.weekday() == 5 or date_formated.weekday() == 6):
        print('Please choose a day between Monday and Friday.')
        
    else:
        
        FACTOR_sensitivity = []
        names = []
        POSITION = []

        universe_tag = kwargs.get('universe_tag', None)

        if len(factors) > 3:
            print('The number of factors need to be less than 3.')
        else:   

            if (universe_tag is not None):
                models = [x.name for x in api_instance.get_models(asset_classes = universe_asset_classes, tags=universe_tag)][::2]
            else:
                models = [x.name for x in api_instance.get_models(asset_classes = universe_asset_classes)][::2]

            df_result = pandas.DataFrame(columns = factors + ['Total Sensitivity (Abs)'])

            print('Gathering data for all the models in the universe (it can take a while depending on the universe chosen)')

            for asset in models:
                factor_sensitivities = []
                sensitivity = api_instance.get_model_sensitivities(model=asset,date_from=date,date_to=date,term = term)

                df_sensitivities = pandas.DataFrame()

                if len(sensitivity) > 0:
                    date = [x for x in sensitivity][0]

                    for data in sensitivity[date]:
                        df_sensitivities[str(data['driver_short_name'])]=[data['sensitivity']]


                    total = 0
                    for factor in factors:
                        total += abs(df_sensitivities[factor][0])
                        factor_sensitivities.append(df_sensitivities[factor][0])

                    df_result.loc[asset] = factor_sensitivities + [total]

            if len(df_result) > 0:
                result = df_result.nlargest(size,'Total Sensitivity (Abs)')
                return result
            else:
                if universe_tag is not None:
                    print('There are no models which satisfies the universe asset classes ' + universe_asset_classes + ' and the universe tag ' + universe_tag)
                else:
                    print('There are no models which satisfies the universe asset classes ' + universe_asset_classes)

        
