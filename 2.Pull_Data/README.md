# Pull_Data

These are examples of directly pulling all of the Qi timeseries data across all Asset classes. There are multiple pre-defined functions which will allow the user to pull timeseries data.

e.g
  One example is our 'get_model_data' function which will allow you to output a dataframe with the following columns:

              * Dates - dataframe index. 
              * FVG - model FVG values for each day requested. 
              * Rsq - model Rsq values for each day requested.
              * Model Value - model fair value for each day requested.
              * Percentage Gap - model percentage gap value for each day requested. 
              * Absolute Gap - model absolute gap value for each day requested. 

                            | FVG      | Rsq      | Model Value | Percentage Gap | Absolute Gap
                 2015-01-01 | 0.17090  | 59.10984 | 108.42994   | 1.76668        | 1.95006
                 2015-01-02 | 0.04313  | 59.35062 | 108.84058   | 0.44765        | 0.48942
                 2015-01-05 | -0.21549 | 59.76303 | 108.67810   | -2.28527       | -2.42810   
 
