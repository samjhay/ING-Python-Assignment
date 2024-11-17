import pandas as pd
import numpy as np
import datetime as dt
from typing import Callable


def _read_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath_or_buffer=filepath, delimiter='\t')
    df['date'] = df.date.apply(dt.datetime.strptime, args=['%d/%m/%Y'])
    df.set_index('date', drop=True, inplace=True)

    return df


def _add_shifted_time_column(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """
    shifted_df = (df
                  .shift(-1)
                  .rename({col: 'time_shift' for col in df.columns}, axis=1))

    return pd.concat([df, shifted_df], axis=1)


def _log_shift(time0_value: float, time1_value: float, horizon_days: float) -> float:
    """

    :param time0_value:
    :param time1_value:
    :param horizon_days:
    :return:
    """
    return np.exp(np.log(time1_value / time0_value) * np.sqrt(horizon_days)) - 1


def _calculate_shift_return(df: pd.DataFrame, horizon_days: float, shift_function: Callable) -> pd.DataFrame:
    """

    :param df:
    :param horizon_days:
    :param shift_function:
    :return:
    """
    # the shifted value (row.iloc[1]) corresponds to the previous day's value
    df['shifted_change'] = df.apply(lambda row: shift_function(time0_value=row.iloc[1],
                                                               time1_value=row.iloc[0],
                                                               horizon_days=horizon_days), axis=1)
    return df


def _calculate_pnl_for_shift(df: pd.DataFrame, portfolio_value: float) -> pd.DataFrame:
    """

    :param df:
    :param portfolio_value:
    :return:
    """
    df['pnl_vector'] = df['shifted_change'] * portfolio_value

    return df


def calculate_instrument_pnl_vector(instrument_timeseries: pd.DataFrame, portfolio_value: float,
                                    return_function: Callable, horizon_days: float) -> pd.DataFrame:
    """

    :param instrument_timeseries:
    :param portfolio_value:
    :param return_function:
    :param horizon_days:
    :return:
    """
    instrument_timeseries = _add_shifted_time_column(instrument_timeseries)
    instrument_timeseries = _calculate_shift_return(instrument_timeseries, horizon_days=horizon_days,
                                                    shift_function=return_function)
    return _calculate_pnl_for_shift(df=instrument_timeseries, portfolio_value=portfolio_value)


def _calculate_var_from_total_pnls(total_pnl_vector: pd.Series) -> float:
    """

    :param total_pnl_vector:
    :return:
    """
    sorted_returns = total_pnl_vector.sort_values()
    return sorted_returns.iloc[1] * 0.4 + sorted_returns.iloc[2] * 0.6


def calculate_var(calculation_config: list) -> float:
    """

    :param calculation_config:
    :return:
    """
    portfolio_total_pnl_vector = pd.Series(index=ccy_2_timeseries.index, data=0)
    for (timeseries, _horizon_days, portfolio_value, return_function) in calculation_config:
        component_pnl = calculate_instrument_pnl_vector(instrument_timeseries=timeseries,
                                                        portfolio_value=portfolio_value,
                                                        return_function=return_function,
                                                        horizon_days=_horizon_days)

        portfolio_total_pnl_vector += component_pnl['pnl_vector']

    return _calculate_var_from_total_pnls(total_pnl_vector=portfolio_total_pnl_vector)
