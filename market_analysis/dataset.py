from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm
import datetime as dt
import yfinance as yf
import pandas as pd

from market_analysis.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def get_stock_data(
    ticker: str,
    end_date: tuple,
    days: int | float,
):
    
    end_date = dt.datetime(*end_date)
    start_date = end_date - dt.timedelta(days=days)

    logger.info(f"Loading {ticker} data from {start_date} to {end_date}.")
    df = yf.download(ticker, start=start_date, end=end_date).stack(future_stack=True)
    logger.success(f"Success loading {ticker} data.")

    df.index.names = ["date", "ticker"]
    df.columns = pd.Index([col.lower().replace(" ", "_") for col in df.columns], name="price")
    df.sort_index(ascending=True, inplace=True)
    df.index = df.index.droplevel(level=1)

    return df


if __name__ == "__main__":
    app()
