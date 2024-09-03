import math
from typing import Dict, NamedTuple

class SunPosition(NamedTuple):
    azimuth: float
    altitude: float

class SolarCalculator:
    RAD: float = math.pi / 180
    DEG: float = 180 / math.pi
    J2000: float = 2451545.0 # Julian date for the epoch J2000.0

    @staticmethod
    def sun_position(date: float, lat: float, lng: float) -> Dict[str, float]:
        """
        Calculate the sun's azimuth and altitude for a given date, latitude, and longitude.

        Args:
            date (float): The date and time in milliseconds since the Unix epoch.
            lat (float): The latitude in degrees.
            lng (float): The longitude in degrees.

        Returns:
            Dict[str, float]: A dictionary with 'azimuth' and 'altitude' in radians.
        """
        days = date / 86400000 - 10957.5

        # Solar coordinates
        mean_long = (280.460 + 0.9856474 * days) % 360
        mean_anom = math.radians((357.528 + 0.9856003 * days) % 360)
        ecliptic_long = math.radians(mean_long + 1.915 * math.sin(mean_anom) + 0.020 * math.sin(2 * mean_anom))

        # Obliquity of the ecliptic
        obliquity = math.radians(23.439 - 0.0000004 * days)

        # Right ascension and declination
        sin_ecliptic = math.sin(ecliptic_long)
        ra = math.atan2(math.cos(obliquity) * sin_ecliptic, math.cos(ecliptic_long))
        dec = math.asin(math.sin(obliquity) * sin_ecliptic)

        # Local sidereal time
        gmst = (6.697375 + 0.0657098242 * days + date % 86400000 / 1000) % 24
        lmst = math.radians((gmst * 15 + lng) % 360)

        # Hour angle
        ha = lmst - ra

        # Convert latitude to radians
        lat_rad = math.radians(lat)

        # Calculate azimuth and altitude
        sin_lat, cos_lat = math.sin(lat_rad), math.cos(lat_rad)
        sin_dec, cos_dec = math.sin(dec), math.cos(dec)
        sin_ha, cos_ha = math.sin(ha), math.cos(ha)

        altitude = math.asin(sin_lat * sin_dec + cos_lat * cos_dec * cos_ha)
        azimuth = math.atan2(-sin_ha * cos_dec, sin_dec * cos_lat - sin_lat * cos_dec * cos_ha)

        # Normalize azimuth to [0, 2π)
        azimuth %= 2 * math.pi

        return {
            'azimuth': azimuth,
            'altitude': altitude
        }
