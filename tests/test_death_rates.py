import pandas as pd
import pytest
from itertools import product

from death_rates.data import fetch_raw, fetch_death_rates

from .fixtures import raw_death_rates


def assert_lists_equal(a, b):
    """ Helper to strictly compare lists """
    assert len(a) == len(b)
    assert all(x == y for x, y in zip(a, b))


def test_fetch_raw():
    """
    Let's check if our data is still available and
    according to expectation.
    Normally I would not test external HTTP requests
    as they are dependent on internet connection.
    """
    raw_data = fetch_raw()
    assert 'ISO Code' in raw_data.columns
    assert 'Uncertainty bounds*' in raw_data.columns
    for type_, year in product(('IMR', 'NMR', 'U5MR'), range(1950, 2015 + 1)):
        assert f'{type_}.{year}' in raw_data.columns


def test_fetch_death_rates(raw_death_rates, mocker):
    """
    Test that the death rate data is parsed correctly
    """
    mock_fetch_raw = mocker.patch('death_rates.data.fetch_raw')
    mock_fetch_raw.return_value = raw_death_rates

    death_rates = fetch_death_rates()

    # test structure
    assert_lists_equal(death_rates.index.levels[0], ['DEU', 'CHE'])
    assert_lists_equal(death_rates.index.levels[1], [1970, 1971])
    assert_lists_equal(death_rates.columns, ['U5MR'])

    # test values
    assert death_rates.loc[('DEU', 1970), 'U5MR'] == 5.0
    assert pd.isnull(death_rates.loc[('CHE', 1970), 'U5MR'])
