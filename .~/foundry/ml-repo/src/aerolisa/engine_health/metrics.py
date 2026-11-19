"""Evaluation metrics for RUL prediction."""

from __future__ import annotations

import numpy as np


def rmse(y_true, y_pred) -> float:
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.sqrt(np.mean((y_pred - y_true) ** 2)))


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.asarray(y_pred, float) - np.asarray(y_true, float))))


def nasa_score(y_true, y_pred) -> float:
    """PHM08 asymmetric score, d = pred - true; late (d >= 0) penalised more than early."""
    d = np.asarray(y_pred, float) - np.asarray(y_true, float)
    return float(np.sum(np.where(d < 0, np.exp(-d / 13) - 1, np.exp(d / 10) - 1)))


def late_share(y_true, y_pred, tol: float = 0.0) -> float:
    """Share of predictions that overestimate remaining life (the dangerous error)."""
    d = np.asarray(y_pred, float) - np.asarray(y_true, float)
    return float(np.mean(d > tol))


def interval_coverage(y_true, lo, hi) -> float:
    y = np.asarray(y_true, float)
    return float(np.mean((y >= np.asarray(lo)) & (y <= np.asarray(hi))))


def interval_width(lo, hi) -> float:
    return float(np.mean(np.asarray(hi, float) - np.asarray(lo, float)))


def summary(y_true, y_pred) -> dict:
    return {
        "rmse": round(rmse(y_true, y_pred), 2),
        "mae": round(mae(y_true, y_pred), 2),
        "nasa_score": round(nasa_score(y_true, y_pred), 1),
        "late_share": round(late_share(y_true, y_pred), 3),
    }
