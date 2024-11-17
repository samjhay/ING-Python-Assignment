from enum import Enum
import logging
import numpy as np
from scipy.stats import norm

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('black_scholes_pricer')


class CallPut(str, Enum):
    CALL = 'call'
    PUT = 'put'


class InvalidPriceParametersException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def _black_d2(forward: float, strike: float, time_to_expiry: float, volatility: float) -> float:
    """
    d2 = (ln(F/K) - sigma**2*T) / (sigma*sqrt(T))
       = d1 - sigma*sqrt(t)

    The value of the standard normal cumulative distribution function corresponding to the return between s0 and strike
    under the risk neutral measure.
    :param forward: The discounted value of the underlying asset at expiry time
    :param strike: The value at which the underlying asset can be bought (call) or sold (put)
    :param time_to_expiry: the remaining time between pricing time and expiry time, expressed in years
    :param volatility: The expected log normal volatility of the underlying asset between pricing time and expiry,
           expressed as volatility per year.
    :return: black d2
    """
    d1 = _black_d1(forward=forward, strike=strike, time_to_expiry=time_to_expiry, volatility=volatility)
    return d1 - (volatility * np.sqrt(time_to_expiry))


def _black_d1(forward: float, strike: float, time_to_expiry: float, volatility: float) -> float:
    """
    d1 = (ln(F/K) + sigma**2*T) / (sigma*sqrt(T))

    The value of the standard normal cumulative distribution function corresponding to the return between s0 and strike
    under the risk neutral measure.

    :param forward: The discounted value of the underlying asset at expiry time
    :param strike: The value at which the underlying asset can be bought (call) or sold (put)
    :param time_to_expiry: the remaining time between pricing time and expiry time, expressed in years
    :param volatility: The expected log normal volatility of the underlying asset between pricing time and expiry,
           expressed as volatility per year.
    :return:
    """
    return (np.log(forward / strike) + (0.5 * volatility**2 * time_to_expiry)) / (volatility * np.sqrt(time_to_expiry))


def _black_76(forward: float, strike: float, time_to_expiry: float, volatility: float, interest_rate: float,
              call_put: CallPut | str):
    """

    :param forward:
    :param strike:
    :param time_to_expiry:
    :param volatility:
    :param interest_rate:
    :param call_put:
    :return:
    """
    d1 = _black_d1(forward=forward, strike=strike, time_to_expiry=time_to_expiry, volatility=volatility)
    d2 = _black_d2(forward=forward, strike=strike, time_to_expiry=time_to_expiry, volatility=volatility)
    discount_factor = np.exp(-interest_rate * time_to_expiry)

    logger.debug(f'F={forward}, K={strike}, tte={time_to_expiry}, sigma={volatility}, d1={d1}, d2={d2}, '
                 f'df={discount_factor}')

    if call_put is CallPut.CALL:
        return discount_factor * (forward * norm.cdf(d1) - strike * norm.cdf(d2))
    if call_put is CallPut.PUT:
        return discount_factor * (strike * norm.cdf(-d2) - forward * norm.cdf(-d1))


def black_scholes_price(forward: float, strike: float, time_to_expiry: float, volatility: float,
                        interest_rate: float, call_put: CallPut | str) -> float:
    """

    :param forward:
    :param strike:
    :param time_to_expiry:
    :param volatility:
    :param interest_rate:
    :param call_put:
    :return:
    """
    call_put = call_put if isinstance(call_put, CallPut) else CallPut(call_put)

    if strike == 0.:
        # edge case. Strike __could__ be 0 and the contract would be priceable though Black Scholes would fail.
        if call_put is CallPut.PUT:
            return 0.
        if call_put is CallPut.CALL:
            return forward

    if time_to_expiry <= 0.:
        # edge case if option has expired and it's intrinsic value is required
        if call_put is CallPut.PUT:
            return np.maximum(0, strike - forward)
        if call_put is CallPut.CALL:
            return np.maximum(0, forward - strike)

    if (strike < 0.) \
        or (forward <= 0.) \
        or (volatility <= 0.):
        # negative variables result in 0 valued denominators or logs
        raise InvalidPriceParametersException(f'Negative pricing variable found. Received input:\n'
                                              f'time to strike: {strike}\n'
                                              f'time to forward: {forward}\n'
                                              f'time to volatility: {volatility}\n'
                                              f'All values should be positive (strike can be 0.)')

    return _black_76(forward=forward, strike=strike, time_to_expiry=time_to_expiry, volatility=volatility,
                     interest_rate=interest_rate, call_put=call_put)
