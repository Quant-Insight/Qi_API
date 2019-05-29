## Description

This piece of code retrieves the buckets' sensitivities for a given model (BMW), a given date (2019-01-14) and a given model term (Long Term). 

**Requirements:** 

* Install matplotlib and pandas:

    * Jupyter Notebooks:
    
        ```  
        !pip install matplotlib pandas
        ```
        
    * Command line:
        
        ```
        $ pip install matplotlib pandas
        ```


**Inputs:** For the purpose of this example, the model, the date and the model term are already defined in example_bucket_driver_sensitivities() function.
               
**Output:** A pie chart representing the bucket's sensitivities for BMW on 2019-01-14, based on a Long Term model.
               

## Code

```python
import qi_client
import pandas
from datetime import datetime

# Configure API key authorization: QI API Key
configuration = qi_client.Configuration()

# Add the API Key provided by QI
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'

# Uncomment to set up a proxy
# configuration.proxy = 'http://localhost:3128'

# create an instance of the API class
api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))

#################################################################################################################
#                                                      Functions
#################################################################################################################
# 
# This function retrieves the buckets' sensitivities for a given model, a given date and a given model term. 
def get_bucket_drivers(model, date, term):
    sensitivity = api_instance.get_model_sensitivities(
            model=model,
            date_from=date,
            date_to=date,
            term=term
            )
    
    df_sensitivities = pandas.DataFrame()
    
    for data in sensitivity[date]:
        if data['bucket_name'] in df_sensitivities.columns:
            df_sensitivities[str(data['bucket_name'])][0] = (
                    df_sensitivities[str(data['bucket_name'])][0] +
                    [data['sensitivity']]
                    )
        else:
            df_sensitivities[str(data['bucket_name'])] = [data['sensitivity']]
            
    # Column heading
    df_sensitivities.index = ['Sensitivity']
    
    return df_sensitivities

# This function calls get_bucket_drivers() function to retrieve buckets's sensitivities for BMW on 2019-01-14,
# based on a Long Term model. It creates a pie chart with the data obtained. 
def example_bucket_driver_sensitivities():

    # To retrieve the buckets' sensitivities of a different model, a different date or a different model term,
    # please modify the imputs of get_bucket_drivers() function. 
    bucket_drivers = get_bucket_drivers('BMW',
                                        '2019-01-14',
                                        'Long Term')
    
    # Create Pie Data
    other = abs(bucket_drivers).transpose().nsmallest(5, 'Sensitivity').sum()
    df_other = pandas.DataFrame(other)
    df_other = df_other.rename(index={'Sensitivity': 'Other'},
                               columns={0: 'Sensitivity'})
    
    pie_bucket_drivers = abs(bucket_drivers).transpose().nlargest(10,
                            'Sensitivity')
    
    pie_bucket_drivers = pie_bucket_drivers.append(df_other)
    
    # Create Colours
    import random
    
    number_of_colors = 11
    
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
    
    df_color = pandas.DataFrame({'Color': color})
    df_color.index = pie_bucket_drivers.index.tolist()
    
    # Set up the plotting
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    
    mpl.rcParams['font.size'] = 22
    
    fig = plt.figure(figsize=(12, 12))
    
    ax = plt.subplot(111)
    
    # Data to plot
    labels = pie_bucket_drivers.index.tolist()
    sizes = [100*float(x) for x in pie_bucket_drivers['Sensitivity']]
    colors = df_color.loc[pie_bucket_drivers.index.tolist()]['Color'].tolist()
    
    # Plot
    plt.pie(sizes,
            labels=labels,
            colors=colors,
            autopct='%1.f%%',
            pctdistance=0.84,
            shadow=False,
            explode=(
                    0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05
                    ),
                    startangle=80)
            
    centre_circle = plt.Circle((0, 0), 0.75, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.axis('equal')
    plt.title('BMW Bucket Drivers')
    plt.show()
    
    fig.savefig('Bucket_Drivers_Pie_Chart_BMW.png',
                bbox_inches="tight",
                facecolor=fig.get_facecolor())
    
    
#################################################################################################################
#                                                           Main Code
#################################################################################################################

example_bucket_driver_sensitivities()
```

## Output

![alt text](https://github.com/Quant-Insight/API_Starter_Kit/blob/master/Code_Examples/img/Bucket_Drivers_Pie_Chart_BMW.png "Bucket Driver Sensitivities")
