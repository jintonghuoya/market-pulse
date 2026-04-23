"""Simple trend forecasting — moving average, linear trend."""

import pandas as pd
import numpy as np


def moving_average_forecast(series, window=4, periods=4):
    """Extend a series using trailing moving average.

    Args:
        series: DatetimeIndex Series.
        window: Rolling window size.
        periods: Number of periods to forecast.

    Returns:
        Series with forecast appended.
    """
    ma = series.rolling(window=window).mean()
    last_val = ma.iloc[-1]
    freq = pd.infer_freq(series.index) or "M"
    future_idx = pd.date_range(
        start=series.index[-1], periods=periods + 1, freq=freq
    )[1:]
    forecast = pd.Series([last_val] * periods, index=future_idx, name=series.name)
    return pd.concat([series, forecast])


def linear_trend_forecast(series, periods=4):
    """Simple linear regression extrapolation.

    Args:
        series: DatetimeIndex Series.
        periods: Number of periods to forecast.

    Returns:
        Series with forecast appended.
    """
    clean = series.dropna()
    if len(clean) < 2:
        return series
    x = np.arange(len(clean))
    coeffs = np.polyfit(x, clean.values, 1)
    freq = pd.infer_freq(series.index) or "M"
    future_x = np.arange(len(clean), len(clean) + periods)
    future_vals = np.polyval(coeffs, future_x)
    future_idx = pd.date_range(
        start=series.index[-1], periods=periods + 1, freq=freq
    )[1:]
    forecast = pd.Series(future_vals, index=future_idx, name=series.name)
    return pd.concat([series, forecast])
