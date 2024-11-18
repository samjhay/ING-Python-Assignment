from unittest import TestCase, main
import numpy as np
from black_scholes_option_price import black_scholes_price, InvalidPriceParametersException
from black_scholes_option_price._black_scholes import _black_d1, _black_d2


class TestEndToEnd(TestCase):
    forward = 19.0436671781375
    strike = 17
    time_to_expiry = 0.46027397260274
    volatility = 0.3
    interest_rate = 0.00498754151104

    def test_end_to_end_call(self):
        call_put = 'call'
        bs = black_scholes_price(self.forward, self.strike, self.time_to_expiry, self.volatility, self.interest_rate,
                                 call_put)
        # Excel floating point precision to 15 significant figures
        self.assertAlmostEqual(bs, 2.6968842086815, places=14)

    def test_end_to_end_put(self):
        call_put = 'put'
        bs = black_scholes_price(self.forward, self.strike, self.time_to_expiry, self.volatility, self.interest_rate,
                                 call_put)
        # Excel floating point precision to 15 significant figures
        self.assertAlmostEqual(bs, 0.657903164673872, places=14)


class TestPricing(TestCase):
    forward = 19.04367
    strike = 17
    time_to_expiry = 0.46
    volatility = 0.3
    interest_rate = 0.005

    def test_put_call_parity(self):
        bs_call = black_scholes_price(self.forward, self.strike, self.time_to_expiry, self.volatility,
                                      self.interest_rate, 'call')
        bs_put = black_scholes_price(self.forward, self.strike, self.time_to_expiry, self.volatility,
                                     self.interest_rate, 'put')
        discount_factor = np.exp(self.interest_rate * self.time_to_expiry)
        self.assertAlmostEqual(self.forward - self.strike, discount_factor * (bs_call - bs_put), delta=1e-14)

    def test_negative_time_returns_intrinsic_value(self):
        bs_call = black_scholes_price(self.forward, self.strike, -1, self.volatility,
                                      self.interest_rate, 'call')
        self.assertEqual(bs_call, self.forward - self.strike)

    def test_negative_vol_throws(self):
        self.assertRaises(InvalidPriceParametersException, black_scholes_price, self.forward, self.strike,
                          self.time_to_expiry, -1 * self.volatility, self.interest_rate, 'call')

    def test_zero_strike_put_worth_zero(self):
        bs_put = black_scholes_price(self.forward, 0, self.time_to_expiry, self.volatility,
                                     self.interest_rate, 'put')
        self.assertEqual(bs_put, 0)

    def test_itm_call_worth_more_than_intrinsic(self):
        bs_call = black_scholes_price(self.forward, self.strike, self.time_to_expiry, self.volatility,
                                      self.interest_rate, 'call')

        self.assertGreater(bs_call, self.forward - self.strike)

    def test_atm_call_equals_put_price(self):
        bs_call = black_scholes_price(self.forward, self.forward, self.time_to_expiry, self.volatility,
                                      self.interest_rate, 'call')
        bs_put = black_scholes_price(self.forward, self.forward, self.time_to_expiry, self.volatility,
                                     self.interest_rate, 'put')
        self.assertEqual(bs_call, bs_put)

    def test_otm_call_put_parity(self):
        upside_strike = 23
        bs_call = black_scholes_price(self.forward, upside_strike, self.time_to_expiry, self.volatility,
                                      self.interest_rate, 'call')
        bs_put = black_scholes_price(self.forward, upside_strike, self.time_to_expiry, self.volatility,
                                     self.interest_rate, 'put')
        discount_factor = np.exp(self.interest_rate * self.time_to_expiry)
        self.assertAlmostEqual(self.forward - upside_strike, discount_factor * (bs_call - bs_put), delta=1e-14)


class TestDs(TestCase):
    forward = 100
    strike = 100
    time_to_expiry = 3
    volatility = 0.2

    def test_d1_greater_than_d2(self):
        for s in [70, 80, 90, 100, 110, 120]:
            with self.subTest():
                d1 = _black_d1(forward=self.forward, strike=s, time_to_expiry=self.time_to_expiry,
                               volatility=self.volatility)
                d2 = _black_d2(forward=self.forward, strike=s, time_to_expiry=self.time_to_expiry,
                               volatility=self.volatility)
                self.assertGreater(d1, d2)


if __name__ == '__main__':
    main()
