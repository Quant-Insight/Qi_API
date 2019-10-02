#######################################################################################################################################
# 
# This function returns the top stocks based on sensitivities (in absolute terms) to a given list of factors. 
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         factor - list of factors. We recommend to use a maximum of 3 factors (e.g. ['USDCNH', 'US GDP', 'Brent'])
#         universe_asset_classes - universe asset class (e.g. 'Equity')
#         size - number of models to be in the result (e.g. 10)
#         date - 'date' (e.g. '2019-05-17')
#         term - 'term' (e.g. 'Long Term')
#         universe_tag (optional) - universe tag (e.g. 'STOXX Europe 600') - The list of the tags can be retrieved using api_instance.get_tags()
#
# Output: 
#         dataframe with the following columns:
#               * Name - top factor drivers' names (10 for our example). 
#               * Factor Sensitivities - one column per factor with the sensitivities values. 
#               * Total Sensitivities (Abs) - Total sum of the sensitivities per model, in absolute terms. 
#               * e.g.
#
#                 |         | USDCNH   | US GDP   | Brent   | Total Sensitivity (Abs) |
#                 |:-------:|:--------:|:--------:|:-------:|:-----------------------:|
#                 | PUM     | -8.89990 | 0.15558  | 2.61010 | 11.66558                | 
#                 | NESTE   | 4.46399  | -0.22389 | 1.41901 | 6.10689                 | 
#                 | ROCKB   | 1.55113  | 0.00471  | 4.26042 | 5.81626                 | 
#                 | CYBG    | 1.00289  | 0.01039  | 4.46287 | 5.47615                 | 
#                 | WG/     | 2.63019  | -0.03145 | 2.75359 | 5.41523                 | 
#                 | NEM EU  | 1.18380  | 0.00282  | 4.13763 | 5.32425                 | 
#                 | NEM GY  | 1.18380  | 0.00282  | 4.13763 | 5.32425                 | 
#                 | WDI     | 1.81811  | -0.00554 | 3.01348 | 4.83713                 | 
#                 | MTRO    | -2.76991 | 0.05251  | 1.53813 | 4.36055                 |
#                 | GVC     | 0.44379  | 0.01903  | 3.78796 | 4.25078                 | 
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

        
