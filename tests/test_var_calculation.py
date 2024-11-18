from unittest import TestCase, main
from var_calculation import calculate_var, read_csv, log_shift


class TestEndToEnd(TestCase):
    def test_end_to_end(self):
        df = read_csv(filepath='../data/ccy_rates.txt')

        ccy_1_timeseries = df.loc[:, ['ccy-1']]
        ccy_2_timeseries = df.loc[:, ['ccy-2']]

        horizon_days = 1

        # timeseries, horizon_days, component value in portfolio, shift function
        portfolio_config = [(ccy_1_timeseries, horizon_days, 153084.81, log_shift),
                            (ccy_2_timeseries, horizon_days, 95891.51, log_shift)]

        var = calculate_var(calculation_config=portfolio_config)

        # Excel stores floating point numbers to 15 significant digits
        self.assertAlmostEqual(var, -13572.7337924684, places=9)


if __name__ == '__main__':
    main()
