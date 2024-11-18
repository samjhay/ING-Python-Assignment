## ING TRM Engineering Assessment
### Sam Haywood

### Answers to Questions
1) Implied volatility is the volatility implied by the price of quoted options. Typically implied volatility
is Black Scholes volatility which is calculated by inverting the Black Scholes price formula to make volatility the output.
The value itself is the market's best estimate for the standard deviation of realisations of the underlying instrument
between pricing time and option expiration. In the Black Scholes case the assumption is made that underlying returns
follows a log-normal distribution with drift. Typically this volatility varies between strikes as market
participants expect larger or smaller volatility at different levels of the underlying.
    Historical volatility is an estimate of the actual standard deviation of price returns of the underlying estimated
from realised price returns and some model assumptions. In the Black Scholes world this results in an estimator such as
sqrt((1/N)*sum(log(S_i/S_(i-1))**2)).
    The difference between the two volatilities is therefore that one is an expectation of future volatility and the other
is an estimate of past volatility for a given underlying product.<br><br>

2) Value at Risk is a tool used by risk management departments to model the expected downside of a portfolio of
financial instruments. VaR gives an estimate for the value of a specified downside percentile over a specified time
frame (for example, the 99% confidence level over 10 days). It gives a X% probability that the portfolio
will lose this value by the next time horizon. The time horizon return (e.g. return over 10 days) is usually estimated
from a single day's return and scaled using sqrt(N days).
    Two groups of methods for calculating VaR are Historical Simulation and Model Building approach. Historical 
Simulation uses past returns as an indicator for future returns. The model building approach involves 
using a Monte Carlo simulation with a current, market-implied volatility surface to incorporate the derivative market's 
expectation into a forward-looking estimate.


### VaR Data Notes
- 24-25th April 2019 ccy 1 has rate 1.56832462754 and 1.57284634, up from 1.15659083286105 the day before
- 27th August 2019 the ccy 1 rate also drops to 1.01012324533 before moving back to the 1.1 area.
- 19th November 2018 the ccy 1 rate is 1.247645328, up from around 1.12 before and after.