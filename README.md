# Racing-Telemetry

Racing-Telemetry is a Python library for analyzing racing data, providing tools for data retrieval, processing, and visualization.

## Installation

You can install the library using pip:

```bash
pip install racing-telemetry
```

## Usage

Here are some examples of how to use the Telemetry library:

### Basic Usage

```python
from racing_telemetry import Telemetry
from racing_telemetry.plot.plots import lap_fig, plot_2d_map
from racing_telemetry.analysis.streaming import Streaming

# Initialize Telemetry
t = Telemetry()

# Set Pandas adapter for data conversion
t.set_pandas_adapter()

# Set filter for specific session and driver
t.set_filter({'session_id': 1719933663, 'driver': 'durandom'})

# Retrieve telemetry data
lap_data = t.get_telemetry_df()

# Calculate average speed
from racing_telemetry.analysis import average_speed
avg_speed = average_speed(lap_data)
print(f"Average speed: {avg_speed:.2f} m/s")

# Create a lap figure
fig = lap_fig(lap_data, columns=["SpeedMs", "Throttle", "Brake"])
fig.show()

# Create a 2D map
map_fig = plot_2d_map(lap_data)
map_fig.show()

# Use streaming analysis
streaming = Streaming()
for index, row in lap_data.iterrows():
    streaming.notify(row.to_dict())
    features = streaming.get_features()
    print(f"Lap time: {row['CurrentLapTime']:.2f}, Average speed: {features['average_speed'][-1]:.2f}, Coasting time: {features['coasting_time'][-1]:.2f}")
```

## Features

- Data retrieval from various sources (GraphQL, InfluxDB, PostgreSQL)
- Data adaptation and conversion
- Basic statistical analysis
- Real-time streaming analysis
- Visualization tools for lap data and track maps

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GPL License - see the LICENSE file for details.
