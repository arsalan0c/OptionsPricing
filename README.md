# OptionsPricing

This python program can be used to for <b>pricing an option</b> or determining <b>implied volatility</b>, with the Black Scholes model.

## Assumptions

* No transaction fees in purchase of option
* Option can only be exercised at expiration
* Periodic daily rate of return can be modelled by Brownian motion
* No arbitrage opportunity exists

## Example Usage

Put option pricing: 
```bash 
python3 BlackScholes.py -s 10 -x 10 -r 0.0.1 -v 0.3 -t 0.25 
```
Call option implied volatility:
```bash 
python3 BlackScholes.py -m impliedvolatility -s 10 -x 10 -r 0.01 -t 0.25 -mp 5.70  
```

## Arguments
```-s``` (float) <i>stock price</i>, <span style="color: red">required</span>

```-x``` (float) <i>strike price</i>, <span style="color: red">required</span>

```-r``` (float) <i>risk-free interest rate</i>, <span style="color: red">required</span>

```-v``` (float) <i>volatility</i>, standard deviation of log returns, <span style="color: orange">required</span> if <b>pricing an option</b>

```-mp``` (float) <i>market price</i> of the option, <span style="color: orange">required</span> if determining <b>implied volatility</b>

```-t``` (float) <i>tau</i>, time to expiry expressed as fraction of year, <span style="color: orange">required</span>. <span style="color: blue">Alternative</span>: ```-ed```

```-ed``` (str) <i>expiry date</i> of option in <i>dd/mm/yyyy</i> format, <span style="color: orange">required</span>. <span style="color: blue">Alternative</span>: ```-t```

```-ot``` (str) <i>option type</i>, ```call``` or ```put```. <span style="color: green">Default</span>: ```call```

```-m``` (str) <i>mode</i>, ```optionprice``` or ```impliedvolatility```. <span style="color: green">Default</span>: ```optionprice```

```-p``` (float) <i>precision</i>, in calculating implied volatility, threshold below which to accept volatility estimate. <span style="color: green">Default</span>: ```optionprice```

```-i``` (int) <i>iterations</i>, in calculating implied volatility, the maximum number of times to run the Newton-Raphson method of successive approximations. <span style="color: green">Default</span>: ```100```
