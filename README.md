# API_Starter_Kit

This repository includes some examples of how to use Quant-Insight's API. 

It contains two main folders:

  * Main_API_functions: contains QI's API functions.
  * Use_Cases_Functions: contains useful examples of how to get the most of QI's API functions. 

## What do you need to start using the API?


* Client Download Token

  * This will be unique to your organisation and is required in order to install the Qi Client. 

* API key

  * If you still don't have an API key, you can contact Quant-Insight. 
  
  * If you already have an API key, insert the following at the start of your script, with your API key instead of 'ADD-YOUR-API-KEY-HERE': 

          import pandas
          import qi_client
          from qi_client.rest import ApiException

          configuration = qi_client.Configuration()

          configuration.api_key['X-API-KEY'] = 'ADD-YOUR-API-KEY-HERE'

          api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))



