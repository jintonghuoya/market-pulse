"""Basic CoStar data analysis utilities."""

import pandas as pd


def summary_stats(df, group_by=None, value_cols=None):
    """Generate summary statistics.

    Args:
        df: Input DataFrame.
        group_by: Column(s) to group by. None = overall stats.
        value_cols: Numeric columns to summarize. None = all numeric.
    """
    if value_cols is None:
        value_cols = df.select_dtypes(include="number").columns.tolist()

    if group_by:
        return df.groupby(group_by)[value_cols].describe()
    return df[value_cols].describe()


def trend(df, date_col, value_col, freq="M"):
    """Compute time series trend.

    Args:
        df: DataFrame with date and value columns.
        date_col: Name of the date column.
        value_col: Name of the value column.
        freq: Resample frequency ('M' monthly, 'Q' quarterly, 'Y' yearly).
    """
    ts = df[[date_col, value_col]].copy()
    ts[date_col] = pd.to_datetime(ts[date_col])
    ts = ts.set_index(date_col).sort_index()
    return ts.resample(freq).mean()
