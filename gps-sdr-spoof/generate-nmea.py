from gpxpy.gpx import GPXTrackPoint
from gpxpy.geo import LocationDelta
import copy
import operator
from math import floor
from datetime import datetime
from datetime import timedelta
from functools import reduce

KNOTS_TO_METERS_PER_SECOND = 0.514444


def nmea_checksum(sentence):
    """
    Compute the checksum for an NMEA sentence

    The sentence may optionally start with a "$" which is ignored and
    may or may not have  a checksum at the end separate by "*"

    The return is a tuple containing the data portion of the sentence which is used to compute teh checksum,
    the value of the checksum, if any, that was passed at the end of the sentence and the
    checksum value that is calculated using the data portion of the sentence
    """
    sentence = sentence.strip().lstrip('$')

    parts = sentence.split('*', 1)
    parts = parts if len(parts) == 2 else (parts[0], None)
    data, checksum = parts
    checksum = int(checksum, 16) if checksum is not None else None

    calc_checksum = reduce(operator.xor, (ord(s) for s in data), 0)

    return data, checksum, calc_checksum


def test_nmea_checksum():
    tests = [("$GPGGA,000000.00,4852.46626694,N,00217.58140440,E,1,05,2.87,+0.00,M,-21.3213,M,,*5E", 0x5e, 0x5e),
             ("GPGGA,000000.00,4852.46626694,N,00217.58140440,E,1,05,2.87,+0.00,M,-21.3213,M,,", None, 0x5e),
             ("$GPGGA,000000.00,4852.46626694,N,00217.58140440,E,1,05,2.87,+0.00,M,-21.3213,M,,", None, 0x5e)
             ]

    for sentence, expected_checksum, expected_calc_checksum in tests:
        data, checksum, calc_checksum  = nmea_checksum(sentence)
        assert (checksum == expected_checksum)
        assert (calc_checksum == expected_calc_checksum)


def generate_gga(time: "datetime",
                 latitude: "Float",
                 longitude: "Float",
                 elevation: "Float"
                ):
    """
    Generate a single GGA NMEA sentence
    """

    # Specify some default values for fields we don't care about
    num_sats = "0"
    hdop = "1.0"
    fix_type = "8"
    geoid_heght = "0.0"
    correction_data_age = ""
    station_id = "0000"

    time_format = '{:0>2}{:0>2}{:0>5.2f}'.format(time.hour, time.minute, time.second + time.microsecond/1000000)

    lat_abs = abs(latitude)
    lat_deg = floor(lat_abs)
    lat_min = (lat_abs - lat_deg) * 60.0
    lat_format = '{:0>2.0f}{:0>11.8f}'.format(lat_deg, lat_min)
    lat_pole = "N" if latitude >= 0 else "S"

    lon_abs = abs(longitude)
    lon_deg = floor(lon_abs)
    lon_min = (lon_abs - lon_deg) * 60
    lon_format = '{:0>3.0f}{:0>11.8f}'.format(lon_deg, lon_min)
    lon_pole = "E" if longitude >= 0 else "W"

    elevation_format = "{:+.2f}".format(elevation or 0.0)

    elements = ["GPGGA", time_format, lat_format, lat_pole, lon_format, lon_pole, fix_type,
                num_sats, hdop, elevation_format, "M", geoid_heght, "M", correction_data_age, station_id]
    sentence = ",".join(elements)
    checksum = nmea_checksum(sentence)[2]
    return "${}*{:02X}".format(sentence, checksum)


def test_generate_gga ():
    expected = "$GPGGA,010101.00,1230.00000000,N,09830.00000000,E,8,0,1.0,+100.00,M,0.0,M,,0000*7D"
    actual = generate_gga(datetime(2020, 1, 1, 1, 1, 1), 12.5, 98.5, 100.0)

    assert (actual == expected)


def gpx2nmea(p: "GPXTrackPoint"):
    """render a GPX point as a GGA NMEA string"""
    return generate_gga(time=p.time, latitude=p.latitude, longitude=p.longitude, elevation=p.elevation)


def interpolate_track_points(p1: "GPXTrackPoint", p2: "GPXTrackPoint", start_time: "datetime", speed: "Float", interval: "Float"):
    """interpolate a path from p1 to p2, moving at speed (knots) with a position every interval seconds"""
    total_distance = p1.distance_2d(p2)
    time_delta = timedelta(seconds=interval)
    dist_delta = speed * KNOTS_TO_METERS_PER_SECOND * interval
    location_delta = LocationDelta(dist_delta, p1.course_between(p2))
    steps = int(round(total_distance / dist_delta))
    p = GPXTrackPoint(latitude=p1.latitude,
                      longitude=p1.longitude,
                      elevation=p1.elevation,
                      time=start_time,
                      speed=speed)
    for i in range(0, steps + 1):
        next_p = copy.deepcopy(p)
        next_p.move(location_delta)
        next_p.adjust_time(time_delta)
        yield p
        p = next_p


def generate_nmea():
    points = interpolate_track_points(GPXTrackPoint(0, 0), GPXTrackPoint(0.01, 0), datetime.utcnow(), 10, 0.1)
    for p in points:
        # print(p)
        print(gpx2nmea(p))


if __name__ == '__main__':
    generate_nmea()
