![ci](https://github.com/luizhenriquelongo/pyiso3166/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/luizhenriquelongo/pycountrycodes/branch/master/graph/badge.svg?token=53G6ZN5K2E)](https://codecov.io/gh/luizhenriquelongo/pycountrycodes)

# PyCountryCodes

PyCountryCodes is a Python library for dealing with the ISO 3166-1 and ISO 3166-2 Standards in a simple way.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `pycountrycodes`.

```bash
pip install pycountrycodes
```

## Usage

### ISO 3166-1

```python
from pycountrycodes import countries

# Go through the full list of countries available.
for country in countries:
    # prints the country name
    print(country.name)

# returns a Country object if the given criteria matches.
countries.get(name='United Kingdom')
countries.get(alpha_2='GB')
countries.get(alpha_3='GBR')

# returns a list of Country options fot the given query using fuzzy search.
countries.search('United Kingdom')

# returns a list of Country options fot the given query using fuzzy search 
# using the match_score_cutoff to filter the list and only return results with
# match_score greater or equal to 70.
countries.search('United Kingdom', match_score_cutoff=70)
```

### ISO 3166-2

```python
from pycountrycodes import subdivisions

# Go through the full list of subdivisions available.
for subdivisions in subdivisions:
    # prints the subdivision name
    print(subdivisions.name)

# returns a Subdivision object if the given criteria matches.
subdivisions.get(code='US-NY')

# returns a list of Subdivision objects if the given criteria matches.
# for name, type and country_code, this method will return a list of options since
# there can be multiples Subdivision objects with the same attribute values.
subdivisions.get(name='New York')  # returns all Subdivision where obj.name is 'New York'
subdivisions.get(type='Province')  # returns all Subdivision where obj.type is 'Province'
subdivisions.get(country_code='GB')  # returns all Subdivision where obj.country_code is 'GB'

# returns a list of Subdivisions options fot the given query using fuzzy search.
subdivisions.search('New York')

# returns a list of Subdivision options fot the given query using fuzzy search 
# using the match_score_cutoff to filter the list and only return results with
# match_score greater or equal to 70.
subdivisions.search('New York', match_score_cutoff=70)
```

### ISO 4127

```python
from pycountrycodes import currencies

# Go through the full list of currencies available.
for currency in currencies:
    # prints the currency name
    print(currency.name)

# returns a Currency object if the given criteria matches.
currencies.get(alpha_3='USD')

# returns a list of Currencies objects if the given criteria matches.
# for name this method will return a list of options since
# there can be multiples Currency objects with the same attribute values.
currencies.get(name='Leone')  # returns all Currency where obj.name is 'Leone'

# returns a list of Currencies options fot the given query using fuzzy search.
currencies.search('Dollar')

# returns a list of Currency options fot the given query using fuzzy search 
# using the match_score_cutoff to filter the list and only return results with
# match_score greater or equal to 70.
currencies.search('Dollar', match_score_cutoff=70)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
