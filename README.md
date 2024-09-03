# Solar Position Calculator

This tool is designed to efficiently compute the sun's azimuth and altitude for any specified date, latitude, and longitude. It is particularly optimized for use in environments with limited computational resources, such as microcontrollers.

## Prerequisites

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/solar-position-calculator.git
   cd solar-position-calculator
   ```

2. **Install the required dependencies**:

   - **Astropy**: Used for verifying the accuracy of solar position calculations.

   - **Alive-progress**: Provides a progress bar for test execution.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Solar Calculator

The `SolarCalculator` class provides a method to compute the sun's position:

```python
from calc import SolarCalculator

calculator = SolarCalculator()
timestamp = 1672531199000  # Example timestamp in milliseconds
latitude = 37.7749  # Example latitude
longitude = -122.4194  # Example longitude

position = calculator.sun_position(timestamp, latitude, longitude)
print(f"Azimuth: {position['azimuth']:.4f} radians, Altitude: {position['altitude']:.4f} radians")
```

### Testing

The `test.py` script validates the solar position calculations against the Astropy library:

```bash
python test.py
```

This script will display a progress bar and print the average and maximum errors for azimuth and altitude in degrees.

```python
# Example test results for 10,000 iterations
avg_azimuth_error: 0.0145 degrees
avg_altitude_error: 0.0016 degrees
max_azimuth_error: 2.4773 degrees
max_altitude_error: 0.0379 degrees
```

## License

This project is open-source and available under the [MIT License](LICENSE.md).

## Contributing

Contributions are welcome. If you have suggestions for improvements or find any issues, please feel free to open an issue or submit a pull request.
