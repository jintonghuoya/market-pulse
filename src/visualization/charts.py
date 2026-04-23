"""Chart generation — trend lines, bar charts, heatmaps."""

from pathlib import Path
import pandas as pd

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def trend_line(series, title="", ylabel="", save_path=None):
    """Plot a single time series as a line chart."""
    if not HAS_MPL:
        raise ImportError("matplotlib required: pip install matplotlib")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(series.index, series.values, marker="o", markersize=3)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return fig


def bar_comparison(df, title="", ylabel="", save_path=None):
    """Bar chart for comparing values across categories.

    df should be a Series with category labels as index.
    """
    if not HAS_MPL:
        raise ImportError("matplotlib required: pip install matplotlib")
    fig, ax = plt.subplots(figsize=(10, 5))
    df.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return fig


def multi_trend(df, title="", ylabel="", save_path=None):
    """Plot multiple series (each column = one line)."""
    if not HAS_MPL:
        raise ImportError("matplotlib required: pip install matplotlib")
    fig, ax = plt.subplots(figsize=(12, 6))
    for col in df.columns:
        ax.plot(df.index, df[col], label=col, marker="o", markersize=2)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.legend(loc="best")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return fig
