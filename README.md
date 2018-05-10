# Description

Loads global death rates between 1970 and 2015 and provides data via HTTP.

# Usage

## Start Server

```
./run.sh
```

## Query API

```
curl -i "http://127.0.0.1:8080/mortality_rate?country_code=DEU&year=1970&year=1971&mr_type=U5MR"
```

The API returns a JSON with mean mortality rate as `mean_mr`.

If there is no data for a given country and year, `warnings.nan` contains those years.
