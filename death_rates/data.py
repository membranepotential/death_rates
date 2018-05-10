"""
Fetch death rates from the interwebs
Provide tidy dataframe
"""

from io import BytesIO
from typing import Tuple

from flask import g
import pandas as pd
import requests

from death_rates import app


DEATH_RATES_URL = \
    'https://sejdemyr.github.io/r-tutorials/basics/data/RatesDeaths_AllIndicators.xlsx'


@app.before_request
def load_death_rates():
    """ Load the death rates into the app context """
    g.death_rates = fetch_death_rates()


def fetch_raw():
    """
    Fetch the mortality rate indicators.
    Returns raw data as pd.DataFrame
    """
    response = requests.get(DEATH_RATES_URL)
    return pd.read_excel(BytesIO(response.content), skiprows=6)


def fetch_death_rates():
    """
    Provides mortality rates of types `IMR`, `NMR`, `U5MR`
    as pd.DataFrame, indexed by country ISO code and year
    """
    death_rates = fetch_raw()

    # index by ISO code
    death_rates = death_rates.set_index('ISO Code')

    # select columns for the `IMR`, `NMR`, `U5MR` indicators
    # and keep only rows with median rates
    relevant_columns = [col for col in death_rates.columns if any(type_ in col for type_ in ('U5MR', 'IMR', 'NMR'))]
    death_rates = death_rates.loc[(death_rates['Uncertainty bounds*'] == 'Median'), relevant_columns]

    # generate MultiIndex for ISO code and year
    split_cols = [split_type_year(col) for col in death_rates.columns]
    death_rates.columns = pd.MultiIndex.from_tuples(split_cols, names=['type', 'year'])
    death_rates = death_rates.stack(dropna=False)

    return death_rates


def split_type_year(col: str) -> Tuple[str, int]:
    """
    Helper to split the columns of the raw death rates dataframe
    Example:
    >>> split_type_year('U5MR.1970')
    ('U5MR', 1970)
    """
    type_, year = col.split('.')
    return (type_, int(year))
