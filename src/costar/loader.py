"""CoStar data loader — reads exported Excel/CSV files from data/costar/."""

from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "costar"


def list_files(suffix=None):
    """List available CoStar data files.

    Args:
        suffix: Filter by extension (e.g. '.xlsx'). None = all supported formats.
    """
    supported = {".xlsx", ".xls", ".csv"}
    if suffix:
        return sorted(DATA_DIR.glob(f"*{suffix}"))
    return sorted(
        f for f in DATA_DIR.iterdir() if f.suffix.lower() in supported
    )


def load(filename=None):
    """Load a CoStar data file into a DataFrame.

    Args:
        filename: Specific file name, or None to load all files and return a dict.

    Returns:
        DataFrame if filename given, dict[str, DataFrame] otherwise.
    """
    if filename:
        path = DATA_DIR / filename
        return _read_file(path)

    frames = {}
    for f in list_files():
        try:
            frames[f.name] = _read_file(f)
        except Exception as e:
            print(f"Warning: failed to read {f.name}: {e}")
    return frames


def _read_file(path):
    """Read a single file into a DataFrame."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    elif path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")
