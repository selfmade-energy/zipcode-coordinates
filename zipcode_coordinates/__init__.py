from .data.de import coordinates
from .exceptions import ZipCodeNotFound
from .version import last_update


__version__ = f"0.1.1.{last_update}"


def get_coordinates_for_zipcode(zipcode):
    """
    Return the coordinates for a given zipcode.

    :param zipcode: The zipcode to look up.
    :return: A tuple of latitude and longitude.
    """

    try:
        return coordinates[str(zipcode)]
    except KeyError:
        raise ZipCodeNotFound(zipcode) from None
