import pytest

from death_rates import app

from .fixtures import raw_death_rates


@pytest.fixture
def client(raw_death_rates, mocker):
    """ Return test client with mocked data """
    mock_fetch_raw = mocker.patch('death_rates.data.fetch_raw')
    mock_fetch_raw.return_value = raw_death_rates

    return app.test_client()


def test_mortality_rate(client):
    """ Test API endpoint """
    endpoint = '/mortality_rate?country_code=DEU&mr_type=U5MR&year=1970'
    response = client.get(endpoint)
    data = response.json

    assert data['country_code'] == 'DEU'
    assert data['mr_type'] == 'U5MR'
    assert data['years'] == [1970]
    assert data['mean_mr'] == pytest.approx(5.0)
    assert not data['warnings']


def test_mortality_rate_multi_years(client):
    """ Test with multiple years """
    endpoint = '/mortality_rate?country_code=DEU&mr_type=U5MR&year=1970&year=1971'
    response = client.get(endpoint)
    data = response.json

    assert data['country_code'] == 'DEU'
    assert data['mr_type'] == 'U5MR'
    assert data['years'] == [1970, 1971]
    assert data['mean_mr'] == pytest.approx(5.5)
    assert not data['warnings']


def test_mortality_rate_no_year(client):
    """ Test with no year """
    endpoint = '/mortality_rate?country_code=DEU&mr_type=U5MR'
    response = client.get(endpoint)
    data = response.json

    assert data['country_code'] == 'DEU'
    assert data['mr_type'] == 'U5MR'
    assert data['years'] == [1970, 1971]
    assert data['mean_mr'] == pytest.approx(5.5)
    assert not data['warnings']


def test_mortality_rate_nans(client):
    """ Test warning if data contains nans """
    endpoint = '/mortality_rate?country_code=CHE&mr_type=U5MR'
    response = client.get(endpoint)
    data = response.json

    assert data['country_code'] == 'CHE'
    assert data['mr_type'] == 'U5MR'
    assert data['years'] == [1970, 1971]
    assert data['mean_mr'] == pytest.approx(3.0)
    assert data['warnings'] == {'nan': [1970]}


def test_mortality_rate_missing_country(client):
    """ Test error for unknown country """
    endpoint = '/mortality_rate?mr_type=U5MR'
    response = client.get(endpoint)
    data = response.json

    assert response.status_code == 422
    assert data['error'] == 'MissingParameter'
    assert data['message'] == 'country_code'


def test_mortality_rate_unknown_country(client):
    """ Test error for unknown country """
    endpoint = '/mortality_rate?country_code=USA&mr_type=U5MR'
    response = client.get(endpoint)
    data = response.json

    assert response.status_code == 422
    assert data['error'] == 'InvalidParameter'
    assert data['message'] == 'country_code unknown'


def test_mortality_rate_missing_type(client):
    """ Test error for unknown type """
    endpoint = '/mortality_rate?country_code=DEU'
    response = client.get(endpoint)
    data = response.json

    assert response.status_code == 422
    assert data['error'] == 'MissingParameter'
    assert data['message'] == 'mr_type'


def test_mortality_rate_unknown_type(client):
    """ Test error for unknown type """
    endpoint = '/mortality_rate?country_code=DEU&mr_type=ABC'
    response = client.get(endpoint)
    data = response.json

    assert response.status_code == 422
    assert data['error'] == 'InvalidParameter'
    assert data['message'] == 'mr_type unknown'


def test_mortality_rate_unknown_year(client):
    """ Test error for unknown year """
    endpoint = '/mortality_rate?country_code=DEU&mr_type=U5MR&year=3000'
    response = client.get(endpoint)
    data = response.json

    assert response.status_code == 422
    assert data['error'] == 'InvalidParameter'
    assert data['message'] == 'no data for year: 3000'
