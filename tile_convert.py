from math import log, tan, radians, cos, pi, floor, degrees, atan, sinh


def sec(x):
    return(1/cos(x))


def latlon_to_xyz(lat, lon, z):
    tile_count = pow(2, z)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return(tile_count*x, tile_count*y)


def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
    return(floor(x_min), floor(x_max),
           floor(y_min), floor(y_max))


def mercatorToLat(mercatorY):
    return(degrees(atan(sinh(mercatorY))))


def y_to_lat_edges(y, z, h=1):
    """

    :param y:
    :param z:
    :param h: specify height of image (i.e. number of tiles in height)
    :return:
    """
    tile_count = pow(2, z)
    unit = 1 / tile_count
    relative_y1 = y * unit
    relative_y2 = relative_y1 + (unit*h)
    lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
    lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
    return(lat1, lat2)


def x_to_lon_edges(x, z, w=1):
    """

    :param x:
    :param z:
    :param w: specify width of image (i.e. number of tiles in width)
    :return:
    """
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon1 = -180 + x * unit
    lon2 = lon1 + (unit*w)
    return(lon1, lon2)


def tile_edges(x, y, z, w=1, h=1):
    lat1, lat2 = y_to_lat_edges(y, z, h)
    lon1, lon2 = x_to_lon_edges(x, z, w)
    return[lon1, lat1, lon2, lat2]
