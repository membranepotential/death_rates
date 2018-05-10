import pytest
import pandas as pd

@pytest.fixture
def raw_death_rates():
    mock_columns = [
        'ISO Code',
        'Uncertainty bounds*',
        'U5MR.1970',
        'U5MR.1971',
        'other'
    ]

    mock_data = [
        ['DEU', 'Median', 5.0, 6.0, 'bla'],
        ['DEU', 'Lower', 3.0, 4.0, 'blub'],
        ['CHE', 'Median', float('nan'), 3.0, 'blab']
    ]

    return pd.DataFrame(data=mock_data, columns=mock_columns)
