```
#######################################################################################################################################
# 
# This function pulls the data to create a Tactical Asset Allocation (TAA) chart. TAA compares Inflation vs Economic Growth for a 
# given universe of assets, taking snapshots of the first day of each month, for the past 12 months. 
#
# Requirements:
#         import Qi_wrapper
#         import pandas
#         from datetime import datetime,timedelta
#         from dateutil.relativedelta import relativedelta
# 
# Inputs: 
#         universe - Universe of stocks to choose from (e.g. ['FinSub Credit'])
#
# Output: 
#         dataframe with the following columns:
#               * Date - First business day of each month, for the past 12 months.
#               * Model - Asset model name. 
#               * Inflation - Sensitivities to Inflation (%). 
#               * Economic Growth - Sentisitivies to Economic Growth (%). 
#               * FVG - Fair Value Gap (stdev)
#               * Rsq - Model Confidence (%)
#               * color - Green if FVG<0. Red if FVG > 0
#               * opacity - Full opacity (1) if Rsq > 65 (the asset is in Macro regime). Half opacity (0.5) if Rsq < 65 (not in Macro regime)
#               * Abs_FVG - FVG in absolute terms (stdev) -> This is used to determine the size of the bubbles. 
#               * e.g.
#
#             
#  |    Date    |       Model     |    Inflation  |   Economic Growth |   FVG    |      Rsq   |   color   |   opacity |  Abs_FVG | 
#  |------------|:---------------:|:-------------:|:-----------------:|:--------:|:----------:|:---------:|:---------:|:--------:|
#  | 2022-07-01 |   FinSub Credit |     4.25965   |     -1.02326      |  0.75017 |   89.45689 |  #C3423F  |       1   |  0.75017 | 
#  | 2022-08-01 |   FinSub Credit |     3.97254   |      0.06424      |  0.19365 |   86.13906 |  #C3423F  |       1   |  0.19365 | 
#  | 2022-09-01 |   FinSub Credit |     3.93689   |      0.40389      |  0.61370 |   79.15580 |  #C3423F  |       1   |  0.61370 | 
#  | 2022-10-03 |   FinSub Credit |     4.10553   |     -0.75933      |  0.22458 |   80.85060 |  #C3423F  |       1   |  0.22458 | 
#  | 2022-11-01 |   FinSub Credit |     2.99549   |      5.04176      | -0.73674 |   71.21545 |    green  |       1   |  0.73674 | 
#  | 2022-12-01 |   FinSub Credit |     3.07601   |      0.13947      | -0.04620 |   87.86449 |    green  |       1   |  0.04620 | 
#  | 2023-01-02 |   FinSub Credit |     5.46220   |     -2.94689      | -0.13818 |   87.97831 |    green  |       1   |  0.13818 | 
#  | 2023-02-01 |   FinSub Credit |     6.13980   |     -2.40436      |  0.00444 |   93.00861 |  #C3423F  |       1   |  0.00444 | 
#  | 2023-03-01 |   FinSub Credit |     5.39560   |     -3.06798      | -0.25878 |   95.61448 |    green  |       1   |  0.25878 | 
#  | 2023-04-03 |   FinSub Credit |     5.47268   |     -2.76149      |  0.52473 |   92.87617 |  #C3423F  |       1   |  0.52473 | 
#  | 2023-05-01 |   FinSub Credit |     6.06210   |     -1.31371      |  0.37152 |   89.86457 |  #C3423F  |       1   |  0.37152 | 
#  | 2023-06-01 |   FinSub Credit |     5.50428   |     -1.19680      | -0.47917 |   86.74478 |    green  |       1   |  0.47917 | 
#  | 2023-07-03 |   FinSub Credit |    -0.01514   |      8.93639      | -0.10270 |   89.54379 |    green  |       1   |  0.10270 | 
#
#######################################################################################################################################

```

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/taa_example.png" alt="Case Study"/>
</br>

```
import Qi_wrapper
import pandas
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

def get_first_mondays_in_range():

    one_year_ago = yearsago(years = 1)
    start_date  = one_year_ago.replace(day=1)
    end_date = datetime.today().replace(day=1)

    dates= pandas.date_range(start_date,end_date , freq='1M')-pandas.offsets.MonthBegin(1)

    weekdays_dates = []

    for date in dates:

        if date.weekday() == 5:
            weekdays_dates.append(date + timedelta(2))

        elif date.weekday() == 6:
            weekdays_dates.append(date + timedelta(1))

        else:
            weekdays_dates.append(date)

    final_dates = [date.strftime('%Y-%m-%d') for date in weekdays_dates]

    if end_date.weekday() == 5:
        end_date = end_date + timedelta(2)

    elif end_date.weekday() == 6:
        end_date = end_date + timedelta(1)

    final_dates.append(end_date.strftime('%Y-%m-%d'))

    return final_dates


def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    return from_date - relativedelta(years=years)


def get_taa_data(universe):

    final_dates = get_first_mondays_in_range()
    df_final = pandas.DataFrame(columns = ['Date', 'Model', 'Inflation', 'Economic Growth', 'FVG', 'Rsq'])

    qi_universe = [model.name for model in api_instance.get_models()[::2]]

    models_to_check = [model for model in universe if model in qi_universe]

    for model in models_to_check:

        asset_class = api_instance.get_model(model).asset_class

        if asset_class != 'FX' and asset_class != 'Crypto':

            df_model_data = Qi_wrapper.get_model_data(model, final_dates[0], final_dates[0], 'Long Term')[['FVG', 'Rsq']]

            if len(df_model_data) > 0:

                df_model_data.index = df_model_data.index.strftime('%Y-%m-%d')

                if asset_class == 'Commodities':
                    df_aux = Qi_wrapper.get_bucket_grid(model, final_dates[0], final_dates[0], 'Long Term')
                    df = pandas.DataFrame({'Inflation': [0], 'Economic Growth': df_aux['Economic Growth'].tolist()}, index = df_aux.index.tolist())
                
                else:
                    try:
                        df = Qi_wrapper.get_bucket_grid(model, final_dates[0], final_dates[0], 'Long Term')[['Inflation', 'Economic Growth']]

                    except:
                        df = pandas.DataFrame({'Inflation': [''], 'Economic Growth': ['']})

                df = pandas.concat([df, df_model_data], axis = 1)

            else:
                df = pandas.DataFrame(columns= ['Inflation', 'Economic Growth', 'FVG', 'Rsq'])

            for date in final_dates[1:]:

                df_aux_model_data = Qi_wrapper.get_model_data(model, date, date, 'Long Term')[['FVG', 'Rsq']]

                if len(df_aux_model_data) > 0:

                    df_aux_model_data.index = df_aux_model_data.index.strftime('%Y-%m-%d')
                    
                    asset_class = api_instance.get_model(model).asset_class

                    if asset_class == 'Commodities':
                        df_aux1 = Qi_wrapper.get_bucket_grid(model, date, date, 'Long Term')
                        df_aux = pandas.DataFrame({'Inflation': [0], 'Economic Growth': df_aux1['Economic Growth'].tolist()}, index = df_aux1.index.tolist())

                    else:
                        try:
                            df_aux = Qi_wrapper.get_bucket_grid(model, date, date, 'Long Term')[['Inflation', 'Economic Growth']]

                        except:
                            df_aux = pandas.DataFrame({'Inflation': [''], 'Economic Growth': ['']})

                    df_aux = pandas.concat([df_aux, df_aux_model_data], axis = 1)
                    df = pandas.concat([df, df_aux], axis = 0, join = 'outer')

            df = df.reset_index().rename({'index':'Date'}, axis = 'columns')
            df.insert(1, 'Model', [model]*len(df))

            df_final = pandas.concat([df_final, df], axis = 0, join = 'outer')
        else:
            print(model + ' is an ' + asset_class + ', and cannot be added to this chart.')

 
    color = ['green' if fvg<0 else '#C3423F' for fvg in df_final['FVG']]
    opacity = [1 if rsq > 65 else 0.5 for rsq in df_final['Rsq']]
    abs_fvg = [abs(fvg) for fvg in df_final['FVG']]

    df_final['color'], df_final['opacity'], df_final['Abs_FVG'] = [color, opacity, abs_fvg]

    color = ['green' if fvg<0 else '#C3423F' for fvg in df_final['FVG']]
    opacity = [1 if rsq > 65 else 0.5 for rsq in df_final['Rsq']]
    abs_fvg = [abs(fvg) for fvg in df_final['FVG']]

    df_final['color'], df_final['opacity'], df_final['Abs_FVG'] = [color, opacity, abs_fvg]

    return df_final
``` 