"""
utils.py  –  Shared helpers for MPL Cambodia S6 EDA website
============================================================
Provides:
  - load_data()        : loads and cleans the main BoxMatch CSV
  - PALETTE / COLORS   : consistent colour scheme
  - apply_theme()      : applies the project-wide Matplotlib/Seaborn light theme
  - kda()              : per-row KDA calculation
  - duration_seconds() : convert "MM:SS" → integer seconds
  - role_family()      : simplify multi-role strings to primary role
"""

from __future__ import annotations

import re
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")

# ── Colour palette ────────────────────────────────────────────────────────────
PALETTE = {
    "primary":   "#4f46e5",   # indigo
    "secondary": "#7c3aed",   # violet
    "accent":    "#0284c7",   # sky blue
    "success":   "#16a34a",   # green
    "warning":   "#d97706",   # amber
    "danger":    "#dc2626",   # red
    "bg":        "#f8fafc",   # near-white page background
    "surface":   "#ffffff",   # card / plot background
    "text":      "#1e293b",   # dark slate
    "muted":     "#64748b",   # slate-500
    "border":    "#e2e8f0",   # slate-200
}

TEAM_COLORS = {
    "See You Soon":    "#4f46e5",
    "DRoar Legends":   "#dc2626",
    "CFU Gaming":      "#16a34a",
    "PRO Esports":     "#d97706",
    "Duck Rice Esport":"#0284c7",
    "Team Flash KH":   "#db2777",
    "Team Max":        "#7c3aed",
    "Team SV":         "#ea580c",
}

ROLE_COLORS = {
    "Fighter":   "#ef4444",
    "Tank":      "#3b82f6",
    "Support":   "#22c55e",
    "Marksman":  "#f59e0b",
    "Mage":      "#8b5cf6",
    "Assassin":  "#f97316",
    "Other":     "#94a3b8",
}

WIN_COLORS  = {"Win": "#16a34a", "Lose": "#dc2626"}
QUAL_COLORS = list(TEAM_COLORS.values())

# ── Theme application ─────────────────────────────────────────────────────────
def apply_dark_theme() -> None:
    """Apply the project-wide light Matplotlib / Seaborn theme.
    (Kept as apply_dark_theme() for backward compatibility with .qmd calls.)
    """
    plt.rcParams.update({
        "figure.facecolor":   PALETTE["surface"],
        "axes.facecolor":     "#f8fafc",
        "axes.edgecolor":     PALETTE["border"],
        "axes.labelcolor":    PALETTE["text"],
        "axes.titlecolor":    "#0f172a",
        "axes.titlesize":     13,
        "axes.titleweight":   "bold",
        "axes.labelsize":     10,
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "axes.grid":          True,
        "grid.color":         "#e2e8f0",
        "grid.linewidth":     0.8,
        "grid.alpha":         0.9,
        "xtick.color":        PALETTE["muted"],
        "ytick.color":        PALETTE["muted"],
        "xtick.labelsize":    9,
        "ytick.labelsize":    9,
        "legend.facecolor":   "#ffffff",
        "legend.edgecolor":   PALETTE["border"],
        "legend.labelcolor":  PALETTE["text"],
        "legend.fontsize":    9,
        "text.color":         PALETTE["text"],
        "figure.titlesize":   15,
        "figure.titleweight": "bold",
        "figure.dpi":         130,
        "figure.figsize":     (10, 5),
        "savefig.facecolor":  PALETTE["surface"],
        "savefig.bbox":       "tight",
        "savefig.dpi":        130,
        "font.family":        "sans-serif",
        "font.sans-serif":    ["Inter", "DejaVu Sans", "Arial"],
    })
    sns.set_theme(
        style="whitegrid",
        rc={
            "axes.facecolor":   "#f8fafc",
            "figure.facecolor": PALETTE["surface"],
            "grid.color":       "#e2e8f0",
        },
    )

# Also expose as apply_theme for clarity
apply_theme = apply_dark_theme

# Activate immediately on import
apply_dark_theme()


# ── Data helpers ──────────────────────────────────────────────────────────────
_DATA_DIR = Path(__file__).parent.parent / "Data"


def _clean_team(name: str) -> str:
    return str(name).strip().rstrip("\r\n ")


def duration_seconds(t: str) -> int:
    """Convert 'MM:SS' string to total seconds (int)."""
    try:
        parts = str(t).strip().split(":")
        return int(parts[0]) * 60 + int(parts[1])
    except Exception:
        return np.nan


def role_family(role: str) -> str:
    """Map multi-role strings to a single primary role."""
    r = str(role).strip()
    for primary in ["Tank", "Fighter", "Marksman", "Support", "Mage", "Assassin"]:
        if r.startswith(primary):
            return primary
    return "Other"


def kda(row) -> float:
    """Classic KDA: (K + A) / max(D, 1)."""
    return (row["K"] + row["A"]) / max(row["D"], 1)


def load_data() -> pd.DataFrame:
    """
    Load and clean the main BoxMatch dataset.

    Returns a tidy DataFrame with extra derived columns:
      - dur_sec   : match duration in seconds
      - dur_min   : match duration in minutes (float)
      - kda       : (K + A) / max(D, 1)
      - role      : simplified primary role
      - team_clean: stripped team name
    """
    path = _DATA_DIR / "MPL Cambodia Season 6 - BoxMatch.csv"
    df = pd.read_csv(path)

    # ── Normalise column names ────────────────────────────────────────────────
    df.columns = (
        df.columns
          .str.strip()
          .str.replace(r"\s+", " ", regex=True)
    )
    # Rename awkward buff columns (handles both raw and stripped variants)
    rename_map = {}
    for col in df.columns:
        col_stripped = col.strip()
        if "Biru" in col_stripped:
            rename_map[col] = "Blue Buff"
        elif "Merah" in col_stripped:
            rename_map[col] = "Red Buff"
        elif col_stripped == "Lord":
            rename_map[col] = "Lord"  # ensure no trailing space
    df.rename(columns=rename_map, inplace=True)

    # ── Team name cleanup ──────────────────────────────────────────────────────
    df["team_clean"] = df["Team"].apply(_clean_team)

    # ── Duration ──────────────────────────────────────────────────────────────
    df["dur_sec"] = df["Time"].apply(duration_seconds).astype(float)
    df["dur_min"] = df["dur_sec"] / 60.0

    # ── KDA ───────────────────────────────────────────────────────────────────
    df["kda"] = df.apply(kda, axis=1)

    # ── Role family ───────────────────────────────────────────────────────────
    df["role"] = df["Role Pick"].apply(role_family)

    # ── Win as bool ───────────────────────────────────────────────────────────
    df["win_bool"] = df["Win"].str.strip() == "Win"

    # ── Date parse ────────────────────────────────────────────────────────────
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ── Fill minor NAs ────────────────────────────────────────────────────────
    df["Blue Buff"] = df["Blue Buff"].fillna(0)
    df["Red Buff"]  = df["Red Buff"].fillna(0)

    return df


# ── Match-level aggregation ───────────────────────────────────────────────────
def match_level(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse player rows → one row per (Match, team_clean, Win) with
    summed objectives and averaged performance stats.
    """
    agg = df.groupby(["Match", "team_clean", "Win", "Stage"], as_index=False).agg(
        dur_min    = ("dur_min",   "first"),
        total_K    = ("K",         "sum"),
        total_D    = ("D",         "sum"),
        total_A    = ("A",         "sum"),
        total_gold = ("Gold",      "sum"),
        avg_kda    = ("kda",       "mean"),
        Tower      = ("Tower",     "first"),
        Lord       = ("Lord",      "first"),
        Turtle     = ("Turtle",    "first"),
        Blue_Buff  = ("Blue Buff", "first"),
        Red_Buff   = ("Red Buff",  "first"),
        MVP_count  = ("MVP",       "sum"),
    )
    agg["objectives"] = agg["Tower"] + agg["Lord"] + agg["Turtle"]
    return agg


# ── Plotting utilities ────────────────────────────────────────────────────────
def add_value_labels(ax, fmt="{:.1f}", fontsize=9, color=None) -> None:
    """Annotate bar patches with their height values."""
    for p in ax.patches:
        h = p.get_height()
        if np.isfinite(h) and h > 0:
            ax.annotate(
                fmt.format(h),
                (p.get_x() + p.get_width() / 2, h),
                ha="center", va="bottom",
                fontsize=fontsize,
                color=color or PALETTE["text"],
                fontweight="bold",
            )


def style_ax(ax, title="", xlabel="", ylabel="") -> None:
    """Apply consistent axis decoration."""
    if title:
        ax.set_title(title, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.tick_params(labelsize=9)


def corr_heatmap(df: pd.DataFrame, cols: list[str], title: str = "Correlation Matrix") -> plt.Figure:
    """Render a styled correlation heatmap (light-theme friendly)."""
    corr = df[cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor(PALETTE["surface"])
    ax.set_facecolor(PALETTE["surface"])
    # Indigo (positive) ↔ white ↔ red (negative) — reads clearly on white
    cmap = sns.diverging_palette(230, 20, s=75, l=50, as_cmap=True)
    sns.heatmap(
        corr, mask=~mask, annot=True, fmt=".2f",
        cmap=cmap, center=0, vmin=-1, vmax=1,
        linewidths=0.5, linecolor="#e2e8f0",
        ax=ax,
        annot_kws={"size": 9, "color": "#0f172a"},
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title(title, pad=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    fig.tight_layout()
    return fig
