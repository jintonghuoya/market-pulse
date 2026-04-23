"""Wind data connector — wraps WindPy API for financial/market data."""

from .base import DataConnector

try:
    from WindPy import w
    w.start()
    HAS_WIND = True
except ImportError:
    HAS_WIND = False


class WindConnector(DataConnector):
    """Pull data from Wind terminal via WindPy.

    Requires Wind terminal running and WindPy installed.
    """

    def list_files(self):
        """Not applicable for Wind — data comes from API."""
        if not HAS_WIND:
            raise ImportError("WindPy not installed. Install from Wind terminal.")
        return []

    def load(self, codes, fields, start_date, end_date=""):
        """Pull data from Wind.

        Args:
            codes: Wind codes or list of codes (e.g. "M0067615" or ["M0067615", "M0067616"]).
            fields: Fields to pull (e.g. ["CLOSE", "VOLUME"]).
            start_date: Start date string "YYYY-MM-DD".
            end_date: End date string "YYYY-MM-DD", default today.

        Returns:
            DataFrame with dates as index, codes as columns.
        """
        if not HAS_WIND:
            raise ImportError("WindPy not installed. Install from Wind terminal.")
        import pandas as pd

        if isinstance(codes, str):
            codes = [codes]
        if isinstance(fields, str):
            fields = [fields]

        result = w.wsd(codes, fields, start_date, end_date)
        if result.ErrorCode != 0:
            raise ValueError(f"Wind error {result.ErrorCode}: {result.Data}")

        df = pd.DataFrame(
            {code: vals for code, vals in zip(codes, result.Data)},
            index=pd.to_datetime(result.Times),
        )
        df.index.name = "date"
        return df

    def wset(self, table, **params):
        """Run a Wind wset query (e.g. sector constituents).

        Args:
            table: Wind table name (e.g. "sectorconstituent").
            **params: Additional parameters for the query.

        Returns:
            DataFrame of results.
        """
        if not HAS_WIND:
            raise ImportError("WindPy not installed.")
        import pandas as pd

        param_str = ";".join(f"{k}={v}" for k, v in params.items())
        result = w.wset(table, param_str)
        if result.ErrorCode != 0:
            raise ValueError(f"Wind error {result.ErrorCode}")

        return pd.DataFrame(
            result.Data, index=result.Fields
        ).T
