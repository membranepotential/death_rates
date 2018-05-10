""" Error handling """

from flask import jsonify

from death_rates import app


class DeathRatesException(Exception):
    """ Base class for errors for this API """
    def __init__(self, status_code, error, message):
        self.status_code = status_code
        self.payload = {
            'error': error,
            'message': message
        }


class MissingParameter(DeathRatesException):
    """
    Exception that is raised when a required url parameter is missing
    """
    def __init__(self, message):
        super().__init__(422, type(self).__name__, message)


class InvalidParameter(DeathRatesException):
    """
    Exception that is raised when an url parameter could not be validated
    """
    def __init__(self, message):
        super().__init__(422, type(self).__name__, message)


@app.errorhandler(DeathRatesException)
def handle_death_rates_exception(error):
    """ Let flask handle a DeathRatesException """
    response = jsonify(error.payload)
    response.status_code = error.status_code
    return response
