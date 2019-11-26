#######################################################################################################################################
# 
# This function finds the Qi model names associated with your Bloomberg tickers.
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         tickers - e.g. ['AAPL US Equity', 'FB US Equity', 'GOOG US Equity']
#
# Output: 
#         dataframe with the following columns:
#               * Tickers - dataframe index. 
#               * Qi Model Name. 
#               * e.g.
#
#                |                | Qi Model Name |
#                | AAPL US Equity |        AAPL   | 
#                | FB US Equity   |          FB   | 
#                | GOOG US Equity |        GOOG   | 
#
#######################################################################################################################################


def get_model_names_from_tickers(tickers):

    ### Load US Equities from API

    API_US = [x.name for x in api_instance.get_models(asset_classes='Equity',tags='USD')][::2]


    ### Load other Equities from API

    API_other = [x.name for x in api_instance.get_models(asset_classes='Equity')][::2]
    [API_other.remove(model) for model in API_US]


    model_names = []

    for ticker in tickers:

        ### Check US tickers

        if any([x in ticker for x in [' US ',' UN ',' UW ']]):

            temp_model = ticker.split(' ')[0]

            if temp_model in API_US:
                model_names.append(temp_model)

            elif temp_model + ' US' in API_US:
                model_names.append(temp_model + ' US')

            else:
                model_names.append(None)



        ### Check other tickers

        else:

            potential_models = [model for model in API_other if model.split(' ')[0] in [x.split(' ')[0] for x in tickers]]
            potential_tickers = [api_instance.get_model(model).definition.instrument1.ticker for model in potential_models]

            if ticker in potential_tickers:
                idx = potential_tickers.index(ticker)
                model_names.append(potential_models[idx])

            else:

                model_names.append(None)
                
    return pandas.DataFrame(model_names,tickers, columns = ['Qi Model Name'])
