# Jakarta Air Quality Dashboard

Dashboard interaktif untuk monitoring kualitas udara Jakarta (ISPU) dari tahun 2010-2025 dengan visualisasi komprehensif dan analisis mendalam.

![Dashboard Preview](https://img.shields.io/badge/Panel-Dashboard-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## Features

- 📊 **KPI Metrics**: Monitor total pengukuran, rata-rata ISPU, hari berkualitas baik, dan polutan kritis
- 📈 **Visualisasi Interaktif**: 
  - Tren ISPU harian
  - Distribusi kategori kualitas udara
  - Tren kategori per tahun
  - Pola musiman dengan heatmap
  - Perbandingan polutan antar stasiun
  - Box plot distribusi polutan
- 🎛️ **Filter Dinamis**: Filter berdasarkan tahun, stasiun, dan kategori kualitas udara
- 📍 **5 Stasiun Monitoring**:
  - DKI1 (Bunderan HI)
  - DKI2 (Kelapa Gading)
  - DKI3 (Jagakarsa)
  - DKI4 (Lubang Buaya)
  - DKI5 (Kebon Jeruk)

## Tech Stack

- **Panel**: Framework dashboard interaktif
- **HvPlot**: Visualisasi data high-level
- **Holoviews**: Library visualisasi declarative
- **Bokeh**: Interactive plotting
- **Pandas**: Data manipulation
- **Remix Icon**: Icon library

## Installation

1. Clone repository:
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

Dashboard akan terbuka di browser pada `http://localhost:5006/dashboard`

## Project Structure

```
jakarta-air-quality-dashboard/
├── dashboard.py          # Main dashboard application
├── ispu_dki_all.csv     # Dataset kualitas udara
├── requirements.txt      # Python dependencies
├── README.md            # Documentation
└── .gitignore           # Git ignore rules
```

## Data Description

Dataset berisi pengukuran kualitas udara dengan kolom:
- `tanggal`: Tanggal pengukuran
- `stasiun`: Nama stasiun monitoring
- `pm25`: Particulate Matter 2.5
- `pm10`: Particulate Matter 10
- `so2`: Sulfur Dioxide
- `co`: Carbon Monoxide
- `o3`: Ozone
- `no2`: Nitrogen Dioxide
- `max`: Nilai ISPU maksimum
- `critical`: Polutan paling kritis
- `categori`: Kategori kualitas udara (BAIK, SEDANG, TIDAK SEHAT, dll)

## Screenshots

### Overview Tab
Menampilkan ringkasan data, tren ISPU harian, dan distribusi kategori.

### Analysis Tab
Analisis mendalam dengan heatmap musiman dan tren bulanan.

### Station Tab
Perbandingan polutan antar stasiun dan distribusi nilai.

### Data Tab
Tabel data detail dengan pagination.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Created with ❤️ for better air quality monitoring in Jakarta.

## Acknowledgments

- Data source: DKI Jakarta Air Quality Monitoring
- Icons: [Remix Icon](https://remixicon.com/)
