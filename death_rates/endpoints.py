"""
API for mortality rate data
"""

from flask import g, jsonify, request

from death_rates import app
from death_rates.errors import MissingParameter, InvalidParameter


@app.route('/mortality_rate')
def get_mortality_rate():
    """
    Return mortality rate of given type for given country and some years
    URL Parameters:
     - country_code: ISO code of country
     - mr_type: one of IMR, NMR, U5MR
     - year: e.g. 1970, years for which to get mortality rate,
             optional, multiple allowed
    """
    # parse country code
    try:
        country_code = request.args['country_code']
    except KeyError:
        raise MissingParameter('country_code')

    # validate country code
    if country_code not in g.death_rates.index.levels[0]:
        raise InvalidParameter('country_code unknown')

    # parse mortality rate type
    try:
        mr_type = request.args['mr_type']
    except KeyError:
        raise MissingParameter('mr_type')

    # validate mr_type
    if mr_type not in g.death_rates.columns:
        raise InvalidParameter('mr_type unknown')

    # parse years
    years = set(request.args.getlist('year', type=int))
    if years:
        # validate years
        for year in years:
            if not year in g.death_rates.index.levels[1]:
                raise InvalidParameter(f'no data for year: {year}')
    else:
        # all years requested
        years = g.death_rates.index.levels[1]

    # select requested data
    rows = [(country_code, year) for year in years]
    mr_data = g.death_rates.loc[rows, mr_type]

    # generate warning if data contains NaNs
    nan_years = mr_data[mr_data.isnull()].index.get_level_values(1)

    # make response
    response = {
        'country_code': country_code,
        'mr_type': mr_type,
        'years': list(years),
        'mean_mr': mr_data.mean(),
        'warnings': dict()
    }

    if not nan_years.empty:
        response['warnings']['nan'] = list(nan_years)

    return jsonify(response)
