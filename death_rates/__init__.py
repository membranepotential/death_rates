from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# enable cors to allow frontend access
CORS(app)

import death_rates.data
import death_rates.endpoints
import death_rates.errors
