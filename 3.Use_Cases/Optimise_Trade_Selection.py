#######################################################################################################################################
# 
# This function returns the top stocks based on sensitivities (in absolute terms) to a given list of factors. 
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         factor - list of factors. We recommend to use a maximum of 3 factors (e.g. ['ADXY', 'US GDP', 'Brent'])
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
#                Name |	ADXY     | US GDP   | Brent Total | Sensitivity
#                AGS  | -0.09107 | -0.00024 | 0.22146     | 0.31277
#                ASRNL|	-0.11486 | -0.00086 | 0.19477     | 0.31049
#                STB  |	-0.10449 | -0.00068 | 0.20225     | 0.30742
#                ETL  |	-0.15895 | -0.00156 | 0.14606     | 0.30657
#                BC8  |	-0.10468 | -0.00068 | 0.19653     | 0.30189
#                SAABB|	-0.14782 | -0.00172 | 0.15073     | 0.30027
#                UPM  |	-0.08579 | -0.00010 | 0.21040     | 0.29629
#                FPE3 |	-0.11327 | -0.00138 | 0.18078     | 0.29543
#                ENEL |	0.12556  | 0.00070  | -0.16881    | 0.29507
#                GALE |	-0.08880 | -0.00004 | 0.19907     | 0.28791
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

        
