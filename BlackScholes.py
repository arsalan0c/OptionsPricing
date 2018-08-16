""" 

Legend of Variables
___________________

	s: stock price
	x: strike price
	mp: market price of option
	bs_p: price of an option as per Black Scholes
	r: risk-free interest rate
	sigma: standard deviation of log returns (volatility)
	fs: future stock price
	ts: today's stock price
	u: periodic daily rate of return
	tau: time to expiration in years  
	vega: derivative of option price with respect to volatility
	N(d1): 
		For call option: future value of stock given stock_price >= strike_price at option expiration
		For put option: future value of stock given stock_price < strike_price at option expiration
	N(d2): 
		For call option: P(stock_price >= strike_price) at option expiration
		For put option: P(stock_price < strike_price) at option expiration

"""
import argparse
import math
import operator
import numpy as np
import scipy.stats as stats
from datetime import datetime

def normal_pdf(y, mean=0, sigma=1.0):
	numerator = math.exp((-1 * math.pow((y - mean), 2)) / 2 * math.pow(sigma, 2))
	denominator =  math.sqrt(2.0 * math.pi) * sigma
	return numerator / denominator
 
def normal_cdf(z, mean=0, sigma=1.0):
	return stats.norm.cdf(z, mean, sigma)

def d(s, x, r, sigma, tau, operator=operator.add):
	numerator = math.log(s / x) + operator(r, math.pow(sigma, 2) / 2) * tau
	denominator = sigma * math.sqrt(tau)

	return numerator / denominator

def mean(r, sigma):
	return r - (math.pow(sigma, 2) / 2)

def time_to_expiry(expiry_date):
	""" Calculate time to expiry of option expressed as fraction of year

	Args:
		s (float): stock price
		x (float): strike price
		mp (float): market price of an option
		option_type (str): specify option type: "call" or "put"  

	Returns:
		float: fraction of year

	"""
	expiry_date_lst = list(map(lambda x: int(x), expiry_date.split('/')))
	dd, mm, yyyy = expiry_date_lst[0], expiry_date_lst[1], expiry_date_lst[2]
	expiry = datetime(yyyy, mm, dd, 23, 59, 59)

	current = datetime.now()
	seconds_in_year = 31536000
	return (expiry - current).total_seconds() / seconds_in_year

def option_payoff(s, x, mp, option_type="call"):
	""" Calculate the potential profit if exercised (
			For call option: strike price < stock price, max(s - x, 0) - op
			For put option: strike price > stock price, max(x - s, 0) - op
		)

	Args:
		s (float): stock price
		x (float): strike price
		mp (float): market price of an option
		option_type (str): specify option type: "call" or "put"  

	Returns:
		float: potential profit

	"""
	if option_type is "put":
		return np.maximum(s - x, 0) - op
	else:
		return np.maximum(x - s, 0) - op

def option_price(s, x, r, sigma, tau, option_type="call"):
	""" Calculate option price as per Black Scholes (
			For call option: s * N(d1)] - [x * e^(-r * tau) * N(d2)]
			For put option: x * e^(-r * tau) * N(-d2)] - [s * N(-d1)
		)
		
	Args:
		s (float): stock price
		x (float): strike price
		r (float): risk-free interest rate
		sigma (float): standard deviation of log returns (volatility)
		tau (float): time to option expiration expressed in years
		option_type (str): specify option type: "call" or "put"  

	Returns:
		float: option price

	""" 
	d1 = d(s, x, r, sigma, tau, operator.add)
	d2 = d(s, x, r, sigma, tau, operator.sub)

	if option_type is "put":
		d1 = -1 * d1
		d2 = -1 * d2

	weighted_stock_price = s * normal_cdf(d1)

	# Discount strike price at expiration to present value
	discounted_strike_price = x * math.exp(-r * tau)
	# Multiply by probability of option having value at expiration
	weighted_strike_price = discounted_strike_price * normal_cdf(d2)

	if option_type is "put":
		return weighted_strike_price - weighted_stock_price 
		
	else:
		return weighted_stock_price - weighted_strike_price

def _vega(s, x, r, sigma, tau):
	""" Calculate derivative of option price with respect to volatility
		vega = s * tau^(1/2) * N(d1)

	Args:
		s (float): stock price
		x (float): strike price
		r (float): risk-free interest rate
		sigma (float: standard deviation of log returns (volatility)
		tau (float): time to option expiration expressed in years

	Returns:
		float: vega

	"""

	d1 = d(s, x, r, sigma, tau, operator.add)

	return s * math.sqrt(tau) * normal_pdf(d1)

def implied_volatility(s, x, r, tau, mp, option_type="call", precision=1e-4, iterations=100):
	""" Newton-Raphson method of successive approximations to find implied volatility

	Args:
		s (float): stock price
		x (float): strike price
		r (float): risk-free interest rate
		tau (float): time to option expiration expressed in years
		mp (float): market price of an option
		option_type (str): specify option type: "call" or "put"  
		precision (float): threshold below which to accept volatility estimate
		iterations (int): number of rounds of estimations to conduct

	Returns:
		float: closest estimation for implied volatility

	"""

	# initial estimation
	sigma = 0.5
	for i in range(0, iterations):
		# price of an option as per Black Scholes
		bs_p = option_price(s, x, r, sigma, tau, option_type)
		diff = mp - bs_p
		# check if difference is acceptable
		if (operator.abs(diff) < precision):
			return sigma

		vega = _vega(s, x, r, sigma, tau)
		# update sigma with addition of difference divided by derivative 
		sigma = sigma + (diff / vega)
		print(sigma)

	# closest estimation
	return sigma

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--s', help='float: stock price.', type=float, action='store', required=True)
	parser.add_argument('-x', '--x', help='float: strike price.', type=float, action='store', required=True)
	parser.add_argument('-r', '--r', help='float: risk-free interest rate.', type=float, action='store', required=True)
	parser.add_argument('-v', '--sigma', help='float: in calculating option price, standard deviation of log returns (volatility).', type=float, action='store')
	parser.add_argument('-mp', '--mp', help='float: in calculating implied volatility, the market price of an option.', type=float, action='store')
	parser.add_argument('-t', '--tau', help='float: time to expiration in years.', type=float, action='store')
	parser.add_argument('-ed', '--expirydate', help='str: expiry date of option in dd/mm/yyyy format.', type=str, action='store')
	parser.add_argument('-ot', '--optiontype', help='str: call or put. default: call.', type=str, default="call", action='store')
	parser.add_argument('-m', '--mode', help='str: optionprice or impliedvolatility', type=str, default="optionprice", action='store')
	parser.add_argument('-p', '--precision', help='float: in calculating implied volatility, threshold below which to accept volatility estimate.', type=float, default=1e-4, action='store')
	parser.add_argument('-i', '--iterations', help='int: maximum number of iterations to run the Newton-Raphson approximation method', type=int, default=100, action='store')

	args = parser.parse_args()
	s = args.s
	x = args.x
	r = args.r
	sigma = args.sigma
	if args.tau:
		tau = args.tau
	else:
		tau = time_to_expiry(args.expirydate)
	mp = args.mp
	option_type = args.optiontype
	mode = args.mode
	precision = args.precision
	iterations = args.iterations

	if mode == "impliedvolatility":
		print("Implied Volatility:", implied_volatility(s, x, r, tau, mp, option_type, precision, iterations))
	else:
		print("Option Price:", option_price(s, x, r, sigma, tau, option_type))
	

if __name__ == "__main__":
	main()









