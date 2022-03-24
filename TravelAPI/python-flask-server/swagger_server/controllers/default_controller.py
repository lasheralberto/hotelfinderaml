import connexion
import six

from swagger_server.models.hotel_array import HotelArray  # noqa: E501
from swagger_server import util


def get_cityby_name(cityName=None):  # noqa: E501
    """Find city by name

    Returns the dataframe of the city # noqa: E501

    :param cityName: parameter city
    :type cityName: str

    :rtype: List[HotelArray]
    """
    return 'do some magic!'
