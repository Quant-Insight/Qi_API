########################################################################################################################################################################################################################################################################
# 
# This function creates a table with the sensitivities values of a specific model within a period of time.  
#
# Requirements:
#         import pandas
# 
# Inputs: 
#         model - model (e.g. 'AAPL')
#         start - starting date (e.g. '2015-05-18')
#         end - ending date (e.g. '2016-05-17')
#         term - term (e.g. 'Long Term')
#
# Output: 
#         dataframe with the following columns:
#               * Date - dataframe index. 
#               * A column by Bucket with its sensitivity associated to the model by date.  
#               * e.g.    
#
#                       Corp credit | DM FX    | EM FX   | EM Sov Risk | Energy   | Est. Earnings | Global Growth | Global Real Rates | Infl. Expec. | Metals  | Peripheral EU Sov Risk | QT Expectations | Risk Aversion | Systemic liquidity | Yield Curve Slope
#           2015-05-18| -0.85255    | 0.09951  | 0.02594 | -0.21233    | 0.00756  | -0.01707      | 0.00016       | -0.08437          | 0.24020      | 0.06581 | 0.31894                | 0.00928         | -0.67213      | -0.17100           | 0.00565
#           2015-05-19| -0.84969    | 0.10256  | 0.02483 | -0.21068    | 0.00410  | -0.01702      | -0.00003      | -0.08051          | 0.22902      | 0.06515 | 0.31861                | 0.01267         | -0.66906      | -0.17174           | 0.00556
#           2015-05-20| -0.84547    | 0.10503  | 0.02446 | -0.20628    | 0.00111  | -0.01686      | 0.00002       | -0.07687          | 0.21939      | 0.06361 | 0.31786                | 0.01550         | -0.66267      | -0.17330           | 0.00474
#           ...       | ...         | ...      | ...     | ...         | ...      | ...           | ...           | ...               | ...          | ...     | ...                    | ...             | ...           | ...                | ...
#
########################################################################################################################################################################################################################################################################


def get_bucket_grid(model,start,end,term):
    
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

        print("Gathering data for %s from %s to %s..." % (model,
        date_from,
        date_to))

        sensitivity.update(
        api_instance.get_model_sensitivities(
        model,
        date_from=date_from,
        date_to=date_to,
        term=term
        )
        )
    
    sensitivity_grid = pandas.DataFrame()
    
    dates = [x for x in sensitivity.keys()]
    dates.sort()

    for date in dates:
        
        df_sensitivities = pandas.DataFrame()

        for data in sensitivity[date]:

            if data['bucket_name'] in df_sensitivities.columns:
                df_sensitivities[str(data['bucket_name'])][0] = df_sensitivities[str(data['bucket_name'])][0] + [data['sensitivity']]

            else:
                df_sensitivities[str(data['bucket_name'])]=[data['sensitivity']]

        df_sensitivities = df_sensitivities.rename(index={0:date})
        df_sensitivities = df_sensitivities.sort_index(axis=1)

        if sensitivity_grid.empty:
            sensitivity_grid = df_sensitivities
        else:
            sensitivity_grid = pandas.concat([sensitivity_grid, df_sensitivities], axis = 0, join = 'outer')
            

    return sensitivity_grid
