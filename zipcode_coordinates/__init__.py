import importlib.metadata

from .exceptions import ZipCodeNotFound, CountryCodeNotFound
from .version import last_update


__version__ = f"0.1.0.{last_update}"


def get_coordinates_for_zipcode(zipcode, country_code="DE"):
    """
    Return the coordinates for a given zipcode and country code.

    :param zipcode: The zipcode to look up.
    :param country_code: The country code to look up the zipcode in.
    :return: A tuple of latitude and longitude.
    """
    try:
        coordinates = importlib.import_module(
            f"zipcode_coordinates.data.{country_code}"
        ).coordinates
    except ModuleNotFoundError:
        raise CountryCodeNotFound(country_code) from None

    try:
        return coordinates[str(zipcode)]
    except KeyError:
        raise ZipCodeNotFound(zipcode) from None
