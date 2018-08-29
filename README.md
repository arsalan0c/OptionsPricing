# OptionsPricing

This python program can be used for <b>pricing</b> an <b>option</b> or determining <b>implied volatility</b>, with the Black Scholes model.

## Assumptions

* No transaction fees in purchase of option
* Option can only be exercised at expiration
* Periodic daily rate of return can be modelled by Brownian motion
* No arbitrage opportunity exists

## Example Usage

Put option pricing: 
```bash 
python3 BlackScholes.py -ot put -s 10 -x 10 -r 0.0.1 -v 0.3 -t 0.25 
```
Call option implied volatility:
```bash 
python3 BlackScholes.py -m impliedvolatility -s 10 -x 10 -r 0.01 -t 0.25 -mp 5.70  
```

## Arguments
```-s``` (float) <i>stock price</i>, required

```-x``` (float) <i>strike price</i>, required

```-r``` (float) <i>risk-free interest rate</i>, required

```-v``` (float) <i>volatility</i>, standard deviation of log returns, required if <b>pricing</b> an <b>option</b>

```-mp``` (float) <i>market price</i> of the option, required if determining <b>implied volatility</b>

```-t``` (float) <i>tau</i>, time to expiry expressed as fraction of year, required. Alternative: ```-ed```

```-ed``` (str) <i>expiry date</i> of option in <i>dd/mm/yyyy</i> format, required. Alternative: ```-t```

```-ot``` (str) <i>option type</i>, ```call``` or ```put```. Default: ```call```

```-m``` (str) <i>mode</i>, ```optionprice``` or ```impliedvolatility```. Default: ```optionprice```

```-p``` (float) <i>precision</i>, in calculating <b>implied volatility</b>, threshold below which to accept volatility estimate. Default: ```1e-4```

```-i``` (int) <i>iterations</i>, in calculating <b>implied volatility</b>, the maximum number of times to run the Newton-Raphson method of successive approximations. Default: ```100```
