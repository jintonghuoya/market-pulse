"""Market fundamentals analysis — occupancy, ADR, RevPAR, demand/supply."""

import pandas as pd


def occupancy_trend(df, date_col="period", value_col="occupancy"):
    """Occupancy rate trend over time."""
    if value_col not in df.columns:
        return None
    ts = _to_ts(df, date_col, value_col)
    return {
        "current": _last(ts),
        "yoy_change": _yoy(ts),
        "series": ts,
    }


def adr_trend(df, date_col="period", value_col="adr"):
    """Average Daily Rate trend."""
    if value_col not in df.columns:
        return None
    ts = _to_ts(df, date_col, value_col)
    return {
        "current": _last(ts),
        "yoy_growth": _yoy(ts),
        "series": ts,
    }


def revpar_trend(df, date_col="period", value_col="revpar"):
    """RevPAR trend (Revenue Per Available Room)."""
    if value_col not in df.columns:
        return None
    ts = _to_ts(df, date_col, value_col)
    return {
        "current": _last(ts),
        "yoy_growth": _yoy(ts),
        "series": ts,
    }


def demand_supply(df, date_col="period"):
    """Demand vs supply analysis."""
    result = {}
    if "demand" in df.columns and "supply" in df.columns:
        demand = _to_ts(df, date_col, "demand")
        supply = _to_ts(df, date_col, "supply")
        ratio = demand / supply.replace(0, float("nan"))
        result["demand_supply_ratio"] = {
            "current": _last(ratio),
            "series": ratio,
        }
    if "demand" in df.columns:
        ts = _to_ts(df, date_col, "demand")
        result["demand"] = {
            "latest": _last(ts),
            "yoy_change": _yoy(ts),
            "series": ts,
        }
    if "supply" in df.columns:
        ts = _to_ts(df, date_col, "supply")
        result["supply"] = {
            "latest": _last(ts),
            "yoy_change": _yoy(ts),
            "series": ts,
        }
    return result if result else None


def cap_rate(df, date_col="period", value_col="cap_rate"):
    """Market cap rate analysis."""
    if value_col not in df.columns:
        return None
    ts = _to_ts(df, date_col, value_col)
    return {
        "current": _last(ts),
        "series": ts,
    }


def summary(df, date_col="period"):
    """One-shot summary of all available hospitality fundamentals."""
    result = {}
    for key, func in [
        ("occupancy", occupancy_trend),
        ("adr", adr_trend),
        ("revpar", revpar_trend),
        ("cap_rate", cap_rate),
    ]:
        r = func(df, date_col=date_col)
        if r:
            result[key] = r
    ds = demand_supply(df, date_col=date_col)
    if ds:
        result.update(ds)
    return result


def _to_ts(df, date_col, value_col):
    """Convert columns to a DatetimeIndex Series."""
    ts = df[[date_col, value_col]].copy()
    ts[date_col] = pd.to_datetime(ts[date_col])
    ts = ts.set_index(date_col).sort_index()
    return ts[value_col]


def _last(series):
    """Get last non-NaN value."""
    clean = series.dropna()
    return clean.iloc[-1].item() if len(clean) > 0 else None


def _yoy(series, periods=12):
    """Year-over-year change."""
    if len(series.dropna()) <= periods:
        return None
    return series.pct_change(periods=periods).dropna().iloc[-1].item()
