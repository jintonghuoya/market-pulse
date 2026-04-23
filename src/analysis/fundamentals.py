"""Market fundamentals analysis — vacancy, rent, absorption, supply/demand."""

import pandas as pd


def vacancy_trend(df, date_col="period", value_col="vacancy_rate"):
    """Vacancy rate trend over time."""
    ts = _to_ts(df, date_col, value_col)
    return {
        "current": ts.iloc[-1].item() if len(ts) > 0 else None,
        "yoy_change": ts.pct_change(periods=12).iloc[-1].item() if len(ts) > 12 else None,
        "series": ts,
    }


def rent_trend(df, date_col="period", value_col="avg_rent"):
    """Average rent trend and growth rate."""
    ts = _to_ts(df, date_col, value_col)
    return {
        "current": ts.iloc[-1].item() if len(ts) > 0 else None,
        "yoy_growth": ts.pct_change(periods=12).iloc[-1].item() if len(ts) > 12 else None,
        "series": ts,
    }


def net_absorption(df, date_col="period", value_col="net_absorption"):
    """Net absorption summary."""
    ts = _to_ts(df, date_col, value_col)
    return {
        "latest": ts.iloc[-1].item() if len(ts) > 0 else None,
        "trailing_4q_sum": ts.tail(4).sum().item() if len(ts) >= 4 else ts.sum().item(),
        "series": ts,
    }


def supply_demand_ratio(df, supply_col="new_supply", demand_col="net_absorption", date_col="period"):
    """Supply vs demand ratio. >1 means oversupply."""
    if supply_col not in df.columns or demand_col not in df.columns:
        return None
    supply = _to_ts(df, date_col, supply_col)
    demand = _to_ts(df, date_col, demand_col)
    ratio = supply / demand.replace(0, float("nan"))
    return {
        "latest_ratio": ratio.iloc[-1].item() if len(ratio) > 0 else None,
        "series": ratio,
    }


def summary(df, date_col="period"):
    """One-shot summary of all available fundamentals."""
    result = {}
    for col_name, func, key in [
        ("vacancy_rate", vacancy_trend, "vacancy"),
        ("avg_rent", rent_trend, "rent"),
        ("net_absorption", net_absorption, "absorption"),
    ]:
        if col_name in df.columns:
            result[key] = func(df, date_col=date_col)
    if "new_supply" in df.columns and "net_absorption" in df.columns:
        result["supply_demand"] = supply_demand_ratio(df, date_col=date_col)
    return result


def _to_ts(df, date_col, value_col):
    """Convert columns to a DatetimeIndex Series."""
    ts = df[[date_col, value_col]].copy()
    ts[date_col] = pd.to_datetime(ts[date_col])
    ts = ts.set_index(date_col).sort_index()
    return ts
