# Description

#### This piece of code retrieves the data of a list of given models (models within Stoxx 600), for a given date (2024-02-23) and find the largest valuation gaps accross a given set of assets. 

#### **Requirements:** 

#### * Install matplotlib and pandas:

####     * Jupyter Notebooks:
      
        !pip install matplotlib pandas
        
####     * Command line:
        
         $ pip install matplotlib pandas

#### **Inputs:** For the purpose of this example, the model and the date are already defined in example_valuation_gaps() function. 
               
#### **Output:** A candle chart representing the top valuation gaps for a given date, and a csv file with the top 10 valuation gaps' summary. 
               

#                                                 Functions

#### This function retrieves the time series of a given model, for a given period of time. 

      def get_vals(model, start, end):
          
          year_start = int(start[:4])
          year_end = int(end[:4])
          time_series = []
          
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
              
              time_series += api_instance.get_model_timeseries(
                      model,
                      date_from=date_from,
                      date_to=date_to)
              
          Rsq = [data.rsquare for data in time_series]
          FVG = [data.sigma for data in time_series]
          dates = [data._date for data in time_series]
          
          df = pandas.DataFrame({'Dates': dates, 'Rsq': Rsq, 'FVG': FVG})
          df.set_index('Dates', inplace=True)
          return df

#### This function obtains the top ten valuation gaps of a given model(s), on a given date. 

      def get_top_valuation_gaps(date, models):
          
          FVG_s, ID, Names, Rsq_s = ([] for i in range(4))
          
          for asset in models:
              try:
                  if float(get_vals(asset, date, date)['Rsq'].iloc[0]) > 65:
                      FVG_s.append(float(get_vals(asset, date, date)['FVG'].iloc[0]))
                      ID.append(asset)
                      Names.append(
                              api_instance.get_model(
                                      model=asset
                              ).name
                      )
                              
                      Rsq_s.append(float(get_vals(asset, date, date)['Rsq'].iloc[0]))
              # Skip if data not available
              except (IndexError, TypeError):
                  continue
          
          df_FVG = pandas.DataFrame({'Name': Names, 'FVG': FVG_s, 'Rsq': Rsq_s})
          df_FVG.index = ID
          
         
          top_gaps = pandas.concat([
                  df_FVG.nsmallest(5, 'FVG'), df_FVG.nlargest(5, 'FVG')
          ])
          MAX = []
          MIN = []
          
      
          for asset in top_gaps['Name']:
              MAX.append(max(get_vals(asset, '2015-01-02', date)['FVG']))
              MIN.append(min(get_vals(asset, '2015-01-02', date)['FVG']))
              
          top_gaps['Max'] = MAX
          
      
          top_gaps['Min'] = MIN
          
          
          return top_gaps


#### This function calls get_top_valuation_gaps() function to retrieve the top ten valuation gaps of all the models within S&P 500 and creates a cvs file with a summary of the values obtained, and a candle chart representing the top ten valuation gaps. 


      def example_valuation_gaps():
          
          # To obtain the top ten valuation gaps of another model(s), please modify the input of 
          # get_top_valuation_gaps() function. 
          
      
          data = api_instance.get_models_with_pagination(tags='S&P 500')
      
          models = data['items']
          last_evaluated_key = data.get('last_evaluated_key', None)
      
          while last_evaluated_key:
              data = api_instance.get_models_with_pagination(exclusive_start_key=last_evaluated_key)
              models.extend(data['items'])
              last_evaluated_key = data.get('last_evaluated_key', None)
      
          sp500 = list(set([model['name'] for model in models]))
      
          
          df = get_top_valuation_gaps('2024-02-23', sorted(sp500))
          
        
          
          import matplotlib
          import matplotlib.pyplot as plt
          
          matplotlib.rcParams.update({'errorbar.capsize': 15})
          
          fig = plt.figure(figsize=(10, 7))
          
          ax = plt.subplot()
          
          plt.yticks(fontsize=12)
          plt.xticks(fontsize=12)
          
          ax.axhline(0, color='k', lw=1)
          fig.patch.set_facecolor('#FFFFFF')
          
          ax.errorbar(df['Name'], 
                      df['FVG'],
                      [df['FVG'] - df['Min'], df['Max'] - df['FVG']],
                      fmt='o',
                      ms='20',
                      color='#C3423F',
                      ecolor='#53B2FF',
                      lw=10, 
                      capthick=8,
                      solid_capstyle='round',
                      solid_joinstyle='round')
          
          ax.spines["top"].set_visible(False)
          ax.spines["right"].set_visible(False)
          ax.spines["bottom"].set_visible(False)
          
          ax.tick_params(axis='x', bottom=False, labelbottom=False)
          
          plt.ylabel('FVG', fontsize=18)
          plt.title('Top Valuation Gaps', fontsize=20)
          
          for x in range(0, len(df['Name'][:10])):
              ax.annotate(df['Name'][x], (df['Name'][x], df['Max'][x]+0.12),
                          ha='center',
                          color='k',
                          fontsize=14)
              
          plt.tight_layout()
          
          df.to_csv(path_or_buf='Top_10_Valuation_Gaps.csv',
                   float_format='%.5f',
                   index_label='Model Name',
                   columns=[
                           'Min',
                           'Max',
                           'FVG',
                    ])
          
          fig.savefig('Top_10_Valuation_Gaps.png',
                      bbox_inches="tight",
                      facecolor=fig.get_facecolor())
          
          plt.show()

      example_valuation_gaps()


<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/Top_10_Valuation_Gaps_new.png"/>
</br>
