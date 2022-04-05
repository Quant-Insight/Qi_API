# Model versus spot price.

The example below details how clients can use Qi data via our API to view asset's model value. In this instance we look at the S&P500 and see how the historical model value compares to spot, see the article: https://www.quant-insight.com/fed-policy-trumps-covid-19/ .


The code below provides an example of how to retrieve this data from the API. The bullet point summary shows how a Qi analyst has interpreted the results 

## Case Study: 'Fed Policy trumps Covid-19' - May 2020

* Qi’s model value for the S&P500 is represented by the purple line. The red line shows spot SPX. From the start of 2020 through to mid March the two lines moved in tandem.

* Qi model value bottomed on Mar 16th at 2,454. Over the next six business days it rallied 4.5% and by Mar 23rd - as spot SPX hit its 2,237 low - Qi model value had risen to 2,658.

* On Sunday Mar 15th the Fed slashed rates 100bp to almost zero, re-introduced forward guidance, re-started Quantitative Easing and broadened the mix of assets eligible to be bought, and launched USD swap lines with five major international Central Banks.

* Qi’s SPX model recognized the significance of the huge Fed policy response. The deflationary impact from Covid-19 was still a negative factor – poor economic data and lower inflation expectations were a drag on SPX - but Qi immediately identified that the policy response was a bigger driver and hence moved model value higher

<br>
<img src="https://github.com/Quant-Insight/API_Starter_Kit/blob/master/img/spx_model_vs_spot.PNG" alt="Case Study"/>
</br>

* Code:

      # Requirements - make sure you've set environment variable QI_API_KEY = YOUR_API_KEY
      import Qi_wrapper

      # Set varialbles
      asset = 'S&P500'
      start = '2020-01-01'
      end = '2022-04-04'
      term = 'Long Term'

      model_values = Qi_wrapper.get_model_data(asset,start,end,term)[['Model Value']]
