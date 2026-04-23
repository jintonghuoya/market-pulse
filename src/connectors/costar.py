"""CoStar data connector — reads exported Excel/CSV files."""

from pathlib import Path
import pandas as pd
from .base import DataConnector

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "costar"

SUPPORTED_FORMATS = {".xlsx", ".xls", ".csv"}


class CoStarConnector(DataConnector):
    """Read CoStar data exports from data/costar/ directory."""

    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR

    def list_files(self):
        """List available CoStar data files."""
        if not self.data_dir.exists():
            return []
        return sorted(
            f for f in self.data_dir.iterdir()
            if f.suffix.lower() in SUPPORTED_FORMATS
        )

    def load(self, filename=None):
        """Load CoStar data file(s).

        Args:
            filename: Specific file name, or None to load all.

        Returns:
            DataFrame if filename given, dict[str, DataFrame] otherwise.
        """
        if filename:
            return self._read(self.data_dir / filename)

        frames = {}
        for f in self.list_files():
            try:
                frames[f.name] = self._read(f)
            except Exception as e:
                print(f"Warning: failed to read {f.name}: {e}")
        return frames

    def _read(self, path):
        """Read a single file into DataFrame."""
        if not path.exists():
            raise FileNotFoundError(f"Not found: {path}")
        if path.suffix.lower() in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        elif path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        raise ValueError(f"Unsupported format: {path.suffix}")
