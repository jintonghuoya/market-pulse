"""Base data connector interface."""

from abc import ABC, abstractmethod
from pathlib import Path


class DataConnector(ABC):
    """Abstract base for all data source connectors."""

    @abstractmethod
    def list_files(self):
        """List available data files."""

    @abstractmethod
    def load(self, filename=None):
        """Load data from source. Returns DataFrame or dict of DataFrames."""
