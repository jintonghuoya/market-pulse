"""Time series utilities for market data."""

import pandas as pd


class MarketSeries:
    """Wrapper around a time-indexed DataFrame for market metrics."""

    def __init__(self, df, date_col, value_col):
        self.df = df[[date_col, value_col]].copy()
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        self.df = self.df.set_index(date_col).sort_index()
        self.value_col = value_col

    def resample(self, freq="ME"):
        """Resample to frequency (ME=monthly, QE=quarterly, YE=yearly)."""
        return self.df.resample(freq).mean()

    def yoy(self):
        """Year-over-year change."""
        return self.df.pct_change(periods=12)

    def qoq(self):
        """Quarter-over-quarter change (resample to Q first)."""
        quarterly = self.resample("QE")
        return quarterly.pct_change()

    def rolling_avg(self, window=4):
        """Rolling average (default 4 periods)."""
        return self.df.rolling(window=window).mean()
