# Back testing FVGs as trading signals

The difference between macro-warranted model value & the spot price of any asset is the Qi Fair Value Gap. This FVG can be used as a trading signal given it will highlight times when an asset price has diverged from macro fundamentals. A quant can back-test Qi FVG signals to test their efficacy.

In this example we look at US health care stocks, of which Qi has 173, and test trading these under the following conditions:

* Long only
* Open trade at FVG > 1.5 & RSq > 65
* Close trade at FVG < 0.5


<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/results_table.png" alt="Case Study"/>
</br>

* Code:

Use 'fvg_back_test' function from https://github.com/Quant-Insight/Qi_API/blob/master/3.Use_Cases/FVG_Back_Test.py

     # Chose tickers to test (only showing first 5/173)
     # to get all 173:
     # health_care_models = [x.name for x in api_instance.get_models(tags = 'Health Care, USD')][::2]
     # health_care_tickers = [api_instance.get_model(model).definition.instrument1.ticker for model in health_care_models]
     health_care_tickers = ['A UN Equity','ABBV UN Equity','ABC UN Equity','ABMD UW Equity','ABT UN Equity']
     
     # run function (click the link above to get details on the function)
     fvg_back_test(health_care_tickers,price_data,1.5,0.5,0.65,['Long'],'2009-01-01','2020-07-02','Long Term')
