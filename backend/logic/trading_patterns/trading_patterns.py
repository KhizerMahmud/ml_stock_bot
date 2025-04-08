import pandas as pd
import numpy as np


def bull_flag(prices):
    """
    Detects a Bull Flag pattern.
    Rules:
    - Strong upward trend (flagpole).
    - Consolidation in a downward-sloping channel (flag).
    - Breakout above the flag signals continuation of the uptrend.
    """
    flagpole = (
        prices["close"].iloc[-10:].pct_change().sum() > 0.1
    )  # Strong upward trend
    consolidation = (
        prices["close"].iloc[-5:].mean() < prices["close"].iloc[-10:-5].mean()
    )  # Downward consolidation
    breakout = (
        prices["close"].iloc[-1] > prices["close"].iloc[-5:].max()
    )  # Breakout above flag
    return flagpole and consolidation and breakout


def bear_flag(prices):
    """
    Detects a Bear Flag pattern.
    Rules:
    - Strong downward trend (flagpole).
    - Consolidation in an upward-sloping channel (flag).
    - Breakout below the flag signals continuation of the downtrend.
    """
    flagpole = (
        prices["close"].iloc[-10:].pct_change().sum() < -0.1
    )  # Strong downward trend
    consolidation = (
        prices["close"].iloc[-5:].mean() > prices["close"].iloc[-10:-5].mean()
    )  # Upward consolidation
    breakout = (
        prices["close"].iloc[-1] < prices["close"].iloc[-5:].min()
    )  # Breakout below flag
    return flagpole and consolidation and breakout


def double_top(prices):
    """
    Detects a Double Top pattern.
    Rules:
    - Price hits resistance twice and fails to break through.
    - Confirmation occurs when the price breaks below the neckline (support level).
    """
    resistance = prices["close"].iloc[-10:-5].max()
    second_peak = prices["close"].iloc[-5:].max()
    neckline = prices["close"].iloc[-10:-5].min()
    return (
        abs(resistance - second_peak) < 0.01 * resistance
        and prices["close"].iloc[-1] < neckline
    )


def double_bottom(prices):
    """
    Detects a Double Bottom pattern.
    Rules:
    - Price hits support twice and bounces back.
    - Confirmation occurs when the price breaks above the neckline (resistance level).
    """
    support = prices["close"].iloc[-10:-5].min()
    second_trough = prices["close"].iloc[-5:].min()
    neckline = prices["close"].iloc[-10:-5].max()
    return (
        abs(support - second_trough) < 0.01 * support
        and prices["close"].iloc[-1] > neckline
    )


def head_and_shoulders(prices):
    """
    Detects a Head and Shoulders pattern.
    Rules:
    - Left shoulder, head, and right shoulder form.
    - Confirmation occurs when the price breaks below the neckline.
    """
    left_shoulder = prices["close"].iloc[-15:-10].max()
    head = prices["close"].iloc[-10:-5].max()
    right_shoulder = prices["close"].iloc[-5:].max()
    neckline = min(prices["close"].iloc[-15:-10].min(), prices["close"].iloc[-5:].min())
    return (
        head > left_shoulder
        and head > right_shoulder
        and prices["close"].iloc[-1] < neckline
    )


def inverse_head_and_shoulders(prices):
    """
    Detects an Inverse Head and Shoulders pattern.
    Rules:
    - Left shoulder, head, and right shoulder form.
    - Confirmation occurs when the price breaks above the neckline.
    """
    left_shoulder = prices["close"].iloc[-15:-10].min()
    head = prices["close"].iloc[-10:-5].min()
    right_shoulder = prices["close"].iloc[-5:].min()
    neckline = max(prices["close"].iloc[-15:-10].max(), prices["close"].iloc[-5:].max())
    return (
        head < left_shoulder
        and head < right_shoulder
        and prices["close"].iloc[-1] > neckline
    )


def cup_and_handle(prices):
    """
    Detects a Cup and Handle pattern.
    Rules:
    - Cup forms a rounded bottom.
    - Handle forms a small downward consolidation.
    - Breakout above the handle signals continuation of the uptrend.
    """
    cup = prices["close"].iloc[-20:-10].min() < prices["close"].iloc[-20:-10].mean()
    handle = prices["close"].iloc[-10:].mean() < prices["close"].iloc[-20:-10].mean()
    breakout = prices["close"].iloc[-1] > prices["close"].iloc[-10:].max()
    return cup and handle and breakout


def ascending_triangle(prices):
    """
    Detects an Ascending Triangle pattern.
    Rules:
    - Price forms higher lows while resistance remains constant.
    - Breakout above resistance signals continuation of the uptrend.
    """
    resistance = prices["close"].iloc[-10:].max()
    higher_lows = all(
        prices["close"].iloc[i] > prices["close"].iloc[i - 1] for i in range(-10, -1)
    )
    breakout = prices["close"].iloc[-1] > resistance
    return higher_lows and breakout


def descending_triangle(prices):
    """
    Detects a Descending Triangle pattern.
    Rules:
    - Price forms lower highs while support remains constant.
    - Breakout below support signals continuation of the downtrend.
    """
    support = prices["close"].iloc[-10:].min()
    lower_highs = all(
        prices["close"].iloc[i] < prices["close"].iloc[i - 1] for i in range(-10, -1)
    )
    breakout = prices["close"].iloc[-1] < support
    return lower_highs and breakout


def symmetrical_triangle(prices):
    """
    Detects a Symmetrical Triangle pattern.
    Rules:
    - Price forms lower highs and higher lows.
    - Breakout direction determines the trend continuation.
    """
    lower_highs = all(
        prices["close"].iloc[i] < prices["close"].iloc[i - 1] for i in range(-10, -5)
    )
    higher_lows = all(
        prices["close"].iloc[i] > prices["close"].iloc[i - 1] for i in range(-5, -1)
    )
    breakout = (
        prices["close"].iloc[-1] > prices["close"].iloc[-5:].max()
        or prices["close"].iloc[-1] < prices["close"].iloc[-5:].min()
    )
    return lower_highs and higher_lows and breakout


def rising_wedge(prices):
    """
    Detects a Rising Wedge pattern.
    Rules:
    - Price forms higher highs and higher lows in a converging channel.
    - Breakout below the wedge signals a reversal.
    """
    higher_highs = all(
        prices["close"].iloc[i] > prices["close"].iloc[i - 1] for i in range(-10, -5)
    )
    higher_lows = all(
        prices["close"].iloc[i] > prices["close"].iloc[i - 1] for i in range(-5, -1)
    )
    breakout = prices["close"].iloc[-1] < prices["close"].iloc[-5:].min()
    return higher_highs and higher_lows and breakout


def falling_wedge(prices):
    """
    Detects a Falling Wedge pattern.
    Rules:
    - Price forms lower highs and lower lows in a converging channel.
    - Breakout above the wedge signals a reversal.
    """
    lower_highs = all(
        prices["close"].iloc[i] < prices["close"].iloc[i - 1] for i in range(-10, -5)
    )
    lower_lows = all(
        prices["close"].iloc[i] < prices["close"].iloc[i - 1] for i in range(-5, -1)
    )
    breakout = prices["close"].iloc[-1] > prices["close"].iloc[-5:].max()
    return lower_highs and lower_lows and breakout


def rectangle_pattern(prices):
    """
    Detects a Rectangle pattern.
    Rules:
    - Price bounces between horizontal support and resistance levels.
    - Breakout direction determines the trend continuation.
    """
    support = prices["close"].iloc[-10:].min()
    resistance = prices["close"].iloc[-10:].max()
    breakout = (
        prices["close"].iloc[-1] > resistance or prices["close"].iloc[-1] < support
    )
    return breakout


def pennant(prices, volume):
    """
    Detects a Pennant pattern.
    Rules:
    - Strong trend (flagpole) followed by a small consolidation (pennant).
    - Breakout in the direction of the flagpole signals continuation.
    """
    flagpole = prices["close"].iloc[-20:-10].pct_change().sum() > 0.1
    consolidation = (
        prices["close"].iloc[-10:].std() < prices["close"].iloc[-20:-10].std()
    )
    breakout = prices["close"].iloc[-1] > prices["close"].iloc[-10:].max()
    return flagpole and consolidation and breakout


def rounded_bottom(prices):
    """
    Detects a Rounded Bottom pattern.
    Rules:
    - Price gradually transitions from a downtrend to an uptrend.
    - Breakout above resistance confirms the reversal.
    """
    downtrend = prices["close"].iloc[-20:-10].mean() > prices["close"].iloc[-10:].mean()
    breakout = prices["close"].iloc[-1] > prices["close"].iloc[-10:].max()
    return downtrend and breakout


def triple_top(prices):
    """
    Detects a Triple Top pattern.
    Rules:
    - Price hits resistance three times and fails to break through.
    - Confirmation occurs when the price breaks below the neckline.
    """
    resistance = prices["close"].iloc[-15:].max()
    neckline = prices["close"].iloc[-15:].min()
    return (
        prices["close"].iloc[-1] < neckline
        and len(
            [
                p
                for p in prices["close"].iloc[-15:]
                if abs(p - resistance) < 0.01 * resistance
            ]
        )
        >= 3
    )


def triple_bottom(prices):
    """
    Detects a Triple Bottom pattern.
    Rules:
    - Price hits support three times and bounces back.
    - Confirmation occurs when the price breaks above the neckline.
    """
    support = prices["close"].iloc[-15:].min()
    neckline = prices["close"].iloc[-15:].max()
    return (
        prices["close"].iloc[-1] > neckline
        and len(
            [p for p in prices["close"].iloc[-15:] if abs(p - support) < 0.01 * support]
        )
        >= 3
    )
