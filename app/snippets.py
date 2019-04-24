import pycountry

COUNTRIES_PART = [(country.alpha_2, country.name)
                  for country in pycountry.countries]

COUNTRIES_ALL = ('', 'All Countries')

COUNTRIES = (*COUNTRIES_PART, COUNTRIES_ALL)
