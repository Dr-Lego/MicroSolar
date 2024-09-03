import math
import random
from datetime import datetime, timedelta
from astropy.coordinates import get_sun, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u
import warnings
from calc import SolarCalculator
from alive_progress import alive_bar

def random_date() -> datetime:
    """Generate a random date between 2020 and 2030."""
    start = datetime(2020, 1, 1)
    end = datetime(2030, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def random_location() -> tuple:
    """Generate a random latitude and longitude."""
    return random.uniform(-90, 90), random.uniform(-180, 180)

def astropy_sun_position(date: datetime, lat: float, lng: float) -> dict:
    """Calculate the sun's position using Astropy for a given date and location."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        location = EarthLocation(lat=lat*u.deg, lon=lng*u.deg)
        time = Time(date)
        altaz = AltAz(location=location, obstime=time)
        sun = get_sun(time).transform_to(altaz)
    return {
        'azimuth': sun.az.rad,
        'altitude': sun.alt.rad
    }

def test(num_tests: int = 1000) -> None:
    """Test the SolarCalculator against Astropy and display error statistics."""
    calculator = SolarCalculator()
    azimuth_errors = []
    altitude_errors = []
    max_az_error = max_alt_error = 0

    # Use a progress bar to display test progress
    with alive_bar(num_tests, title="Testing Solar Calculator") as bar:
        for _ in range(num_tests):
            date = random_date()
            lat, lng = random_location()

            timestamp = date.timestamp() * 1000  # Convert to milliseconds
            calc_result = calculator.sun_position(timestamp, lat, lng)
            astro_result = astropy_sun_position(date, lat, lng)

            az_error = calc_result['azimuth'] - astro_result['azimuth']
            alt_error = calc_result['altitude'] - astro_result['altitude']

            # Adjust for circular nature of azimuth
            az_error = min(abs(az_error), abs(2 * math.pi - abs(az_error)))

            azimuth_errors.append(az_error)
            altitude_errors.append(alt_error)

            max_az_error = max(max_az_error, az_error)
            max_alt_error = max(max_alt_error, abs(alt_error))

            bar()  # Update progress bar

    avg_az_error = sum(azimuth_errors) / num_tests
    avg_alt_error = sum(altitude_errors) / num_tests

    results = {
        'avg_azimuth_error': math.degrees(avg_az_error),
        'avg_altitude_error': math.degrees(avg_alt_error),
        'max_azimuth_error': math.degrees(max_az_error),
        'max_altitude_error': math.degrees(max_alt_error)
    }

    print("Test results:")
    for key, value in results.items():
        print(f"{key}: {value:.4f} degrees")

if __name__ == "__main__":
    test(1000)
