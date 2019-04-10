# API_Starter_Kit

This repository includes some examples of how to use Quant-Insight API. 

## What do you need to start using the API?


* Client Download Token

  * This will be unique to your organisation and is required in order to install the Qi Client. 

* API key

  * If you still don't have an API key, you can contact Quant-Insight. 
  
  * If you already have an API key, you just need to add this part of the code at the beginning with your API key instead of 'ADD-YOUR-       API-KEY-HERE': 

          import pandas
          import qi_client
          from qi_client.rest import ApiException

          configuration = qi_client.Configuration()

          configuration.api_key['X-API-KEY'] = 'ADD-YOUR-API-KEY-HERE'

          api_instance = qi_client.DefaultApi(qi_client.ApiClient(configuration))



