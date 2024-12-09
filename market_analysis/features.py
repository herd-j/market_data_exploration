from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm
import pandas as pd
import numpy as np

from market_analysis.config import PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def get_Nday_return(
    df: pd.DataFrame,
    days: int, # Days over which to compute return
    log: bool = False, # Whether log return should be computed or not
    shift: bool = False, # True is useful if creating a target variable for training ML 
):
    
    if not isinstance(days, int):
        raise TypeError(f'days must be of type integer')
    
    # Ensure data is correctly ordered
    df.sort_index(ascending=True, inplace=True)

    logger.info(f"Computing{' log ' if log else ' '}return over {days}")


    if not log:
        RETURN = df["close"].pct_change(days)
        colname = f'RTN_D{days}'
    else:
        RETURN = np.log(df["close"]).diff(days)
        colname = f'LOGRTN_D{days}'
        
    if shift:
        colname = 'FUTURE_' + colname
        df[colname] = RETURN.shift(-days)
    else:
        df[colname] = RETURN

    return df

if __name__ == "__main__":
    app()
