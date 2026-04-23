"""Regional / cross-market comparison analysis."""

import pandas as pd


def compare_markets(df, metric_col, group_col="market", date_col="period"):
    """Compare a metric across markets.

    Returns a DataFrame with one column per market, indexed by date.
    """
    if metric_col not in df.columns or group_col not in df.columns:
        raise ValueError(f"Missing columns: {metric_col} or {group_col}")
    pivot = df.pivot_table(
        index=date_col, columns=group_col, values=metric_col, aggfunc="mean"
    )
    pivot.index = pd.to_datetime(pivot.index)
    return pivot.sort_index()


def rank_markets(df, metric_col, group_col="market", top_n=10, ascending=False):
    """Rank markets by latest value of a metric."""
    if metric_col not in df.columns:
        raise ValueError(f"Column not found: {metric_col}")
    latest = (
        df.sort_values("period")
        .groupby(group_col)
        .last()[metric_col]
        .sort_values(ascending=ascending)
    )
    return latest.head(top_n)


def yoy_comparison(df, metric_col, group_col="market", date_col="period"):
    """Year-over-year change per market."""
    pivot = compare_markets(df, metric_col, group_col, date_col)
    return pivot.pct_change(periods=12)
