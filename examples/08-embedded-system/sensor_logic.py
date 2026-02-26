#!/usr/bin/env python3
"""
Example 8: Embedded System Optimization (Python → Zig)
Original Python sensor data processing for IoT devices
"""

import time
import sys
import json
import math

# Sensor reading structure
class SensorReading:
    def __init__(self, timestamp, temperature, humidity, pressure, light):
        self.timestamp = timestamp
        self.temperature = temperature  # Celsius
        self.humidity = humidity        # Percentage (0-100)
        self.pressure = pressure        # Pascals
        self.light = light              # Lux

# Processed sensor data
class ProcessedData:
    def __init__(self, timestamp, temp_f, dew_point, heat_index,
                 pressure_mmhg, altitude_m, light_level):
        self.timestamp = timestamp
        self.temp_f = temp_f
        self.dew_point = dew_point
        self.heat_index = heat_index
        self.pressure_mmhg = pressure_mmhg
        self.altitude_m = altitude_m
        self.light_level = light_level

def generate_sensor_readings(count=10000):
    """
    Generate simulated sensor readings
    Simulates typical IoT sensor data streams
    """
    import random
    random.seed(42)  # Reproducible

    readings = []
    base_time = int(time.time() * 1000)  # Milliseconds

    for i in range(count):
        # Realistic sensor values with noise
        temperature = 20.0 + random.uniform(-5.0, 15.0) + math.sin(i / 100.0) * 3.0
        humidity = 50.0 + random.uniform(-20.0, 30.0) + math.cos(i / 80.0) * 10.0
        pressure = 101325.0 + random.uniform(-1000.0, 1000.0)  # Standard atmospheric
        light = max(0, 500.0 + random.uniform(-400.0, 400.0))  # Lux

        reading = SensorReading(
            timestamp=base_time + i * 1000,  # 1 second intervals
            temperature=temperature,
            humidity=max(0.0, min(100.0, humidity)),
            pressure=pressure,
            light=light
        )
        readings.append(reading)

    return readings

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return celsius * 9.0 / 5.0 + 32.0

def calculate_dew_point(temperature_c, humidity_percent):
    """
    Calculate dew point using Magnus formula
    Accurate approximation for meteorological applications
    """
    a = 17.27
    b = 237.7

    alpha = ((a * temperature_c) / (b + temperature_c)) + math.log(humidity_percent / 100.0)
    dew_point = (b * alpha) / (a - alpha)

    return dew_point

def calculate_heat_index(temperature_c, humidity_percent):
    """
    Calculate heat index (apparent temperature)
    Based on NOAA formula
    """
    temp_f = celsius_to_fahrenheit(temperature_c)

    # Simple formula for moderate conditions
    if temp_f < 80.0:
        return temperature_c

    # Rothfusz regression (full formula)
    hi = -42.379 + 2.04901523 * temp_f + 10.14333127 * humidity_percent
    hi -= 0.22475541 * temp_f * humidity_percent
    hi -= 0.00683783 * temp_f * temp_f
    hi -= 0.05481717 * humidity_percent * humidity_percent
    hi += 0.00122874 * temp_f * temp_f * humidity_percent
    hi += 0.00085282 * temp_f * humidity_percent * humidity_percent
    hi -= 0.00000199 * temp_f * temp_f * humidity_percent * humidity_percent

    # Convert back to Celsius
    heat_index_c = (hi - 32.0) * 5.0 / 9.0

    return heat_index_c

def pressure_to_mmhg(pressure_pa):
    """Convert Pascals to mmHg (millimeters of mercury)"""
    return pressure_pa / 133.322

def calculate_altitude(pressure_pa, sea_level_pa=101325.0):
    """
    Calculate altitude from barometric pressure
    Using barometric formula
    """
    altitude = 44330.0 * (1.0 - math.pow(pressure_pa / sea_level_pa, 1.0 / 5.255))
    return altitude

def categorize_light(lux):
    """Categorize light level"""
    if lux < 10:
        return "dark"
    elif lux < 50:
        return "dim"
    elif lux < 300:
        return "indoor"
    elif lux < 1000:
        return "bright"
    else:
        return "very_bright"

def process_sensor_reading(reading):
    """
    Process a single sensor reading
    Apply calibration, unit conversions, and derived calculations
    """
    # Temperature conversions
    temp_f = celsius_to_fahrenheit(reading.temperature)

    # Dew point calculation
    dew_point = calculate_dew_point(reading.temperature, reading.humidity)

    # Heat index (apparent temperature)
    heat_index = calculate_heat_index(reading.temperature, reading.humidity)

    # Pressure conversions
    pressure_mmhg = pressure_to_mmhg(reading.pressure)

    # Altitude estimation
    altitude_m = calculate_altitude(reading.pressure)

    # Light level categorization
    light_level = categorize_light(reading.light)

    return ProcessedData(
        timestamp=reading.timestamp,
        temp_f=temp_f,
        dew_point=dew_point,
        heat_index=heat_index,
        pressure_mmhg=pressure_mmhg,
        altitude_m=altitude_m,
        light_level=light_level
    )

def moving_average_filter(values, window_size=5):
    """
    Apply moving average filter for noise reduction
    Commonly used in embedded systems
    """
    if len(values) < window_size:
        return values

    filtered = []
    for i in range(len(values)):
        if i < window_size - 1:
            # Not enough data yet, use what we have
            window = values[:i+1]
        else:
            # Full window
            window = values[i-window_size+1:i+1]

        avg = sum(window) / len(window)
        filtered.append(avg)

    return filtered

def detect_anomalies(readings, threshold_std_dev=2.5):
    """
    Detect anomalous sensor readings
    Using statistical outlier detection
    """
    if len(readings) < 10:
        return []

    # Calculate mean and standard deviation
    temps = [r.temperature for r in readings]
    mean_temp = sum(temps) / len(temps)

    variance = sum((t - mean_temp) ** 2 for t in temps) / len(temps)
    std_dev = math.sqrt(variance)

    # Detect outliers
    anomalies = []
    for i, reading in enumerate(readings):
        deviation = abs(reading.temperature - mean_temp) / std_dev
        if deviation > threshold_std_dev:
            anomalies.append({
                'index': i,
                'timestamp': reading.timestamp,
                'value': reading.temperature,
                'deviation': deviation
            })

    return anomalies

def process_sensor_stream(readings):
    """
    Process a stream of sensor readings
    Main processing pipeline for embedded system
    """
    print("╔══════════════════════════════════════════════╗")
    print("║   Python Sensor Data Processing (IoT)       ║")
    print("╚══════════════════════════════════════════════╝\n")

    print(f"Processing {len(readings)} sensor readings...")

    start_time = time.time()

    # Process each reading
    processed = []
    for i, reading in enumerate(readings):
        result = process_sensor_reading(reading)
        processed.append(result)

        # Progress reporting
        if (i + 1) % 1000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            eta = (len(readings) - i - 1) / rate if rate > 0 else 0
            print(f"  Processed {i + 1}/{len(readings)} | {rate:.2f} readings/sec | ETA: {eta:.1f}s")

    processing_time = time.time() - start_time

    # Apply moving average filter to temperatures
    print("\nApplying moving average filter...")
    filter_start = time.time()
    temps = [r.temperature for r in readings]
    filtered_temps = moving_average_filter(temps, window_size=5)
    filter_time = time.time() - filter_start

    # Detect anomalies
    print("Detecting anomalies...")
    anomaly_start = time.time()
    anomalies = detect_anomalies(readings)
    anomaly_time = time.time() - anomaly_start

    total_time = time.time() - start_time

    # Summary statistics
    avg_temp = sum(p.temp_f for p in processed) / len(processed)
    avg_humidity = sum(r.humidity for r in readings) / len(readings)
    avg_pressure = sum(p.pressure_mmhg for p in processed) / len(processed)

    print(f"\n{'='*60}")
    print("PROCESSING SUMMARY")
    print('='*60)
    print(f"Total readings: {len(readings)}")
    print(f"Total time: {total_time:.3f}s")
    print(f"  Processing: {processing_time:.3f}s ({processing_time/total_time*100:.1f}%)")
    print(f"  Filtering: {filter_time:.3f}s ({filter_time/total_time*100:.1f}%)")
    print(f"  Anomaly detection: {anomaly_time:.3f}s ({anomaly_time/total_time*100:.1f}%)")
    print(f"Throughput: {len(readings) / total_time:.2f} readings/sec")
    print(f"Memory usage (estimate): {sys.getsizeof(readings) / 1024:.2f} KB")

    print(f"\nSensor Averages:")
    print(f"  Temperature: {avg_temp:.2f}°F")
    print(f"  Humidity: {avg_humidity:.2f}%")
    print(f"  Pressure: {avg_pressure:.2f} mmHg")
    print(f"  Anomalies detected: {len(anomalies)}")

    return {
        'num_readings': len(readings),
        'total_time': total_time,
        'processing_time': processing_time,
        'filter_time': filter_time,
        'anomaly_time': anomaly_time,
        'throughput': len(readings) / total_time,
        'anomalies_count': len(anomalies),
        'avg_temp_f': avg_temp,
        'avg_humidity': avg_humidity,
        'avg_pressure_mmhg': avg_pressure
    }

if __name__ == "__main__":
    num_readings = int(sys.argv[1]) if len(sys.argv) > 1 else 10000

    # Generate sensor data
    print("Generating sensor readings...")
    gen_start = time.time()
    readings = generate_sensor_readings(num_readings)
    gen_time = time.time() - gen_start
    print(f"  Generated {len(readings)} readings in {gen_time:.3f}s\n")

    # Process sensor stream
    result = process_sensor_stream(readings)

    # Save benchmark results
    if len(sys.argv) > 2 and sys.argv[2] == '--save':
        result['generation_time'] = gen_time
        with open('python_benchmark.json', 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nBenchmark results saved to python_benchmark.json")
