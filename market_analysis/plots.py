from pathlib import Path

from loguru import logger
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from market_analysis.features import get_Nday_return
import numpy as np
import talib.abstract as ta
from market_analysis.config import FIGURES_DIR, PROCESSED_DATA_DIR


def plot_indicator(
    df: pd.DataFrame,
    indicator: pd.Series,
    indicator_name: str = None,
):

    if indicator_name is None:
        indicator_name = "Technical indicator"

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df.index, y=indicator, name=indicator_name, line=dict(color="darkcyan", width=1.2)
        ),
        secondary_y=True,
        row=1,
        col=1,
    )

    daily_return = get_Nday_return(df, days=1, log=True, append_column=False)
    fig.add_trace(go.Bar(x=df.index, y=daily_return, showlegend=False), secondary_y=False)

    fig.update_traces(
        marker_color=np.where(daily_return > 0, "green", "red"),
        marker_line_width=0.05,
        selector=dict(type="bar"),
    )

    fig.update_layout(
        bargap=0,
        bargroupgap=0,
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=50, r=50, b=50, t=50, pad=2),
        yaxis=dict(title=dict(text="Daily return")),
        yaxis2=dict(title=dict(text=indicator_name), fixedrange=False),
        xaxis=dict(title=dict(text="Date"), fixedrange=False),
        template="plotly_dark",
    )

    fig.update(layout_xaxis_rangeslider_visible=True)

    fig.show()


def plot_indicators(
    df: pd.DataFrame,
    indicators: pd.Series,
):

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    for indicator_name in indicators.columns:

        fig.add_trace(
            go.Scatter(
                x=df.index, y=indicators[indicator_name], name=indicator_name, line=dict(width=1.2)
            ),
            secondary_y=True,
            row=1,
            col=1,
        )

    daily_return = get_Nday_return(df, days=1, log=True, append_column=False)
    fig.add_trace(go.Bar(x=df.index, y=daily_return, showlegend=False), secondary_y=False)

    fig.update_traces(
        marker_color=np.where(daily_return > 0, "green", "red"),
        marker_line_width=0.05,
        selector=dict(type="bar"),
    )

    fig.update_layout(
        bargap=0,
        bargroupgap=0,
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=50, r=50, b=50, t=50, pad=2),
        yaxis=dict(title=dict(text="Daily return")),
        yaxis2=dict(title=dict(text=indicator_name), fixedrange=False),
        xaxis=dict(title=dict(text="Date"), fixedrange=False),
        template="plotly_dark",
    )

    fig.update(layout_xaxis_rangeslider_visible=True)

    fig.show()


def indicator_summary(
    df: pd.DataFrame, indicator_name: str, args: dict = {}, indicators: pd.DataFrame = None
):

    print(ta.Function(indicator_name))
    
    if indicators is None:
        indicators = ta.Function(indicator_name, **args)(df)

    if isinstance(indicators, pd.DataFrame):
        plot_indicators(df, indicators)
    else:
        plot_indicator(df, indicators, indicator_name)
