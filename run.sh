#!/bin/bash

export FLASK_ENV='development'
export FLASK_APP='death_rates'

flask run -h 0.0.0.0 -p 8080
