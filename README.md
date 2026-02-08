# Jakarta Air Quality Dashboard

An interactive dashboard for monitoring Jakarta's air quality (ISPU - Air Pollution Standard Index) from 2010-2025 with comprehensive visualizations and in-depth analysis.

![Dashboard Preview](https://img.shields.io/badge/Panel-Dashboard-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## Features

- 📊 **KPI Metrics**: Track total measurements, average ISPU, good air quality days, and critical pollutants
- 📈 **Interactive Visualizations**: 
  - Daily ISPU trends
  - Air quality category distribution
  - Category trends per year
  - Seasonal patterns with heatmap
  - Pollutant comparison across stations
  - Pollutant distribution box plots
- 🎛️ **Dynamic Filters**: Filter by year, station, and air quality category
- 📍 **5 Monitoring Stations**:
  - DKI1 (Bunderan HI)
  - DKI2 (Kelapa Gading)
  - DKI3 (Jagakarsa)
  - DKI4 (Lubang Buaya)
  - DKI5 (Kebon Jeruk)

## Tech Stack

- **Panel**: Interactive dashboard framework
- **HvPlot**: High-level data visualization
- **Holoviews**: Declarative visualization library
- **Bokeh**: Interactive plotting
- **Pandas**: Data manipulation
- **Remix Icon**: Icon library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jakarta-air-quality-dashboard.git
cd jakarta-air-quality-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard:
```bash
panel serve dashboard.py --show
```

The dashboard will open in your browser at `http://localhost:5006/dashboard`

## Project Structure

```
jakarta-air-quality-dashboard/
├── dashboard.py          # Main dashboard application
├── ispu_dki_all.csv     # Air quality dataset
├── requirements.txt      # Python dependencies
├── README.md            # Documentation
└── .gitignore           # Git ignore rules
```

## Data Description

The dataset contains air quality measurements with the following columns:
- `tanggal`: Measurement date
- `stasiun`: Monitoring station name
- `pm25`: Particulate Matter 2.5
- `pm10`: Particulate Matter 10
- `so2`: Sulfur Dioxide
- `co`: Carbon Monoxide
- `o3`: Ozone
- `no2`: Nitrogen Dioxide
- `max`: Maximum ISPU value
- `critical`: Most critical pollutant
- `categori`: Air quality category (GOOD, MODERATE, UNHEALTHY, etc.)

## Dashboard Tabs

### Overview Tab
Displays data summary, daily ISPU trends, and category distribution.

### Analysis Tab
In-depth analysis with seasonal heatmap and monthly trends.

### Station Tab
Pollutant comparison across stations and value distribution.

### Data Tab
Detailed data table with pagination.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Created with ❤️ for better air quality monitoring in Jakarta.

## Acknowledgments

- Data source: DKI Jakarta Air Quality Monitoring
- Icons: [Remix Icon](https://remixicon.com/)
