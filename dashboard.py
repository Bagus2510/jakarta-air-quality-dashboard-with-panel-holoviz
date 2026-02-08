import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator', 'plotly', css_files=['https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css'])
import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')
from bokeh.models import HoverTool

# Load and prepare data
DF = pd.read_csv("ispu_dki_all.csv", parse_dates=["tanggal"])
DF["Tahun"] = DF["tanggal"].dt.year
DF["Bulan"] = DF["tanggal"].dt.month_name()
DF["Hari"] = DF["tanggal"].dt.day

# Fill NaN values in 'pm25' column with mean
mean_pm25 = DF['pm25'].mean()
DF['pm25'] = DF['pm25'].fillna(mean_pm25)

# Sidebar Filter Widgets
year_filter = pn.widgets.Select(
    name='Pilih Tahun',
    options=['Semua'] + sorted(DF['Tahun'].unique().tolist()),
    value='Semua'
)

station_options = [s for s in DF['stasiun'].unique() if pd.notna(s)]
station_filter = pn.widgets.Select(
    name='Pilih Stasiun',
    options=['Semua'] + station_options,
    value='Semua'
)

category_options = [cat for cat in DF['categori'].unique() if pd.notna(cat)]
category_filter = pn.widgets.Select(
    name='Kategori Kualitas Udara',
    options=['Semua'] + category_options,
    value='Semua'
)

# Reactive Data Filtering Function
def get_filtered_data(year, station, category):
    """Filter dataframe based on widget selections"""
    df_filtered = DF.copy()
    
    # Filter by year
    if year != 'Semua':
        df_filtered = df_filtered[df_filtered['Tahun'] == year]
    
    # Filter by station
    if station != 'Semua':
        df_filtered = df_filtered[df_filtered['stasiun'] == station]
    
    # Filter by category
    if category != 'Semua':
        df_filtered = df_filtered[df_filtered['categori'] == category]
    
    return df_filtered

# Bind the filter function to widgets
filtered_df = pn.bind(
    get_filtered_data,
    year_filter,
    station_filter,
    category_filter
)

# Summary Metrics/KPIs
def create_summary_metrics(data):
    """Generate summary KPI indicators with icons"""
    df = data
    
    # Total measurements
    total_count = len(df)
    
    # Average ISPU
    avg_ispu = df['max'].mean() if len(df) > 0 else 0
    
    # Good days count (BAIK category)
    good_days = len(df[df['categori'] == 'BAIK'])
    
    # Most critical pollutant
    critical_pollutant = df['critical'].mode()[0] if len(df) > 0 and len(df['critical'].mode()) > 0 else 'N/A'
    
    # Create indicators with Remix icons
    kpi_total = pn.pane.HTML(
        f'''<div style="border: 1px solid #e0e0e0; padding: 12px 15px; background: white;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <i class="ri-bar-chart-box-line" style="font-size: 32px; color: #4CAF50;"></i>
                <div>
                    <div style="font-size: 12px; color: #666; margin-bottom: 2px;">Total Pengukuran</div>
                    <div style="font-size: 24px; font-weight: 600; color: #333;">{total_count:,}</div>
                </div>
            </div>
        </div>'''
    )
    
    kpi_avg_ispu = pn.pane.HTML(
        f'''<div style="border: 1px solid #e0e0e0; padding: 12px 15px; background: white;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <i class="ri-dashboard-line" style="font-size: 32px; color: #2196F3;"></i>
                <div>
                    <div style="font-size: 12px; color: #666; margin-bottom: 2px;">Rata-rata ISPU</div>
                    <div style="font-size: 24px; font-weight: 600; color: #333;">{avg_ispu:.1f}</div>
                </div>
            </div>
        </div>'''
    )
    
    kpi_good_days = pn.pane.HTML(
        f'''<div style="border: 1px solid #e0e0e0; padding: 12px 15px; background: white;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <i class="ri-checkbox-circle-line" style="font-size: 32px; color: #00BCD4;"></i>
                <div>
                    <div style="font-size: 12px; color: #666; margin-bottom: 2px;">Hari Berkualitas BAIK</div>
                    <div style="font-size: 24px; font-weight: 600; color: #333;">{good_days:,}</div>
                </div>
            </div>
        </div>'''
    )
    
    kpi_critical = pn.pane.HTML(
        f'''<div style="border: 1px solid #e0e0e0; padding: 12px 15px; background: white;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <i class="ri-alert-line" style="font-size: 32px; color: #FF9800;"></i>
                <div>
                    <div style="font-size: 12px; color: #666; margin-bottom: 2px;">Polutan Paling Kritis</div>
                    <div style="font-size: 24px; font-weight: 600; color: #333;">{critical_pollutant}</div>
                </div>
            </div>
        </div>'''
    )
    
    return pn.Row(kpi_total, kpi_avg_ispu, kpi_good_days, kpi_critical, sizing_mode='stretch_width', align='center')

# Bind metrics to filtered data
summary_metrics = pn.bind(create_summary_metrics, filtered_df)

# Visualizations
def create_time_series_plot(data):
    """Create time series plot of ISPU over time"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    # Aggregate by date to handle multiple stations per day
    daily_avg = df.groupby('tanggal')['max'].mean().reset_index()
    
    plot = daily_avg.hvplot.line(
        x='tanggal',
        y='max',
        title='Tren ISPU dari Waktu ke Waktu',
        xlabel='Tanggal',
        ylabel='ISPU (Max)',
        color='#2196F3',
        line_width=2,
        height=400,
        responsive=True,
        grid=True
    )
    
    return plot

def create_category_bar_chart(data):
    """Create bar chart of air quality categories"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    category_counts = df['categori'].value_counts().reset_index()
    category_counts.columns = ['categori', 'count']
    
    # Define color mapping for categories
    color_map = {
        'BAIK': '#4CAF50',
        'SEDANG': '#FFC107',
        'TIDAK SEHAT': '#FF9800',
        'SANGAT TIDAK SEHAT': '#F44336',
        'TIDAK ADA DATA': '#9E9E9E'
    }
    
    plot = category_counts.hvplot.bar(
        x='categori',
        y='count',
        title='Distribusi Kategori Kualitas Udara',
        xlabel='Kategori',
        ylabel='Jumlah',
        color='categori',
        cmap=color_map,
        height=400,
        responsive=True,
        rot=0
    )
    
    return plot

def create_station_comparison(data):
    """Create grouped bar chart comparing pollutants by station"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    # Calculate average pollutants by station
    station_avg = df.groupby('stasiun')[['pm25', 'pm10', 'so2', 'co', 'o3', 'no2']].mean().reset_index()
    
    # Melt for grouped bar chart
    station_melted = station_avg.melt(id_vars='stasiun', var_name='Polutan', value_name='Rata-rata')
    
    plot = station_melted.hvplot.bar(
        x='stasiun',
        y='Rata-rata',
        by='Polutan',
        title='Perbandingan Polutan per Stasiun',
        xlabel='Stasiun',
        ylabel='Rata-rata Nilai',
        height=450,
        responsive=True,
        rot=0,
        legend='top'
    )
    
    return plot

def create_monthly_heatmap(data):
    """Create heatmap showing ISPU patterns by month and year"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    # Create pivot table for heatmap
    monthly_data = df.groupby(['Tahun', 'Bulan'])['max'].mean().reset_index()
    
    # Ensure proper month ordering
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_data['Bulan'] = pd.Categorical(monthly_data['Bulan'], categories=month_order, ordered=True)
    
    pivot_data = monthly_data.pivot(index='Bulan', columns='Tahun', values='max')
    
    plot = pivot_data.hvplot.heatmap(
        title='Pola ISPU Bulanan per Tahun',
        cmap='RdYlGn_r',
        xlabel='Tahun',
        ylabel='Bulan',
        height=450,
        responsive=True,
        colorbar=True,
        clabel='ISPU'
    )
    
    return plot

def create_pollutant_pie_chart(data):
    """Create horizontal bar chart of critical pollutants distribution"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    critical_counts = df['critical'].value_counts().reset_index()
    critical_counts.columns = ['Polutan', 'Jumlah']
    
    # Sort by count for better visualization
    critical_counts = critical_counts.sort_values('Jumlah', ascending=True)
    
    # Define colors for different pollutants
    color_map = {
        'PM10': '#FF6B6B',
        'PM25': '#FFA500',
        'SO2': '#4ECDC4',
        'CO': '#95E1D3',
        'O3': '#F38181',
        'NO2': '#AA96DA'
    }
    
    plot = critical_counts.hvplot.barh(
        x='Polutan',
        y='Jumlah',
        title='Distribusi Polutan Kritis',
        xlabel='Polutan',
        ylabel='Jumlah Kejadian',
        color='Polutan',
        cmap=color_map,
        height=400,
        responsive=True,
        legend=False,
        rot=0
    )
    
    return plot

def create_monthly_trend(data):
    """Create line plot showing monthly trends"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    # Group by year and month
    monthly_avg = df.groupby(['Tahun', 'Bulan'])['max'].mean().reset_index()
    
    # Ensure proper month ordering
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_avg['Bulan'] = pd.Categorical(monthly_avg['Bulan'], categories=month_order, ordered=True)
    monthly_avg = monthly_avg.sort_values(['Tahun', 'Bulan'])
    
    # Create year-month label
    monthly_avg['Period'] = monthly_avg['Tahun'].astype(str) + '-' + monthly_avg['Bulan'].astype(str).str[:3]
    
    plot = monthly_avg.hvplot.line(
        x='Period',
        y='max',
        by='Tahun',
        title='Tren ISPU Bulanan',
        xlabel='Bulan',
        ylabel='Rata-rata ISPU',
        height=400,
        responsive=True,
        grid=True,
        legend='top_right',
        rot=45
    )
    
    return plot

def create_pollutant_boxplot(data):
    """Create box plot showing distribution of pollutants"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    # Select pollutant columns and melt
    pollutant_cols = ['pm25', 'pm10', 'so2', 'co', 'o3', 'no2']
    pollutant_data = df[pollutant_cols].melt(var_name='Polutan', value_name='Nilai')
    
    plot = pollutant_data.hvplot.box(
        y='Nilai',
        by='Polutan',
        title='Distribusi Nilai Polutan',
        ylabel='Nilai',
        xlabel='Polutan',
        height=400,
        responsive=True,
        legend=False
    )
    
    return plot

def create_category_trend(data):
    """Create line chart of category distribution over time"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    # Group by year and category
    category_trend = df.groupby(['Tahun', 'categori']).size().reset_index(name='count')
    
    # Pivot for line chart
    pivot_cat = category_trend.pivot(index='Tahun', columns='categori', values='count').fillna(0)
    
    # Reset index to make Tahun a column
    pivot_cat = pivot_cat.reset_index()
    
    # Melt for line chart
    melted = pivot_cat.melt(id_vars='Tahun', var_name='Kategori', value_name='Jumlah')
    
    # Define color list matching the category order
    colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336', '#9E9E9E']
    
    plot = melted.hvplot.line(
        x='Tahun',
        y='Jumlah',
        by='Kategori',
        title='Tren Kategori Kualitas Udara per Tahun',
        xlabel='Tahun',
        ylabel='Jumlah Hari',
        height=400,
        responsive=True,
        line_width=2.5,
        color=colors,
        legend='top_right',
        grid=True
    )
    
    return plot

def create_category_trend_all_years(station, category):
    """Create line chart showing all years, filtered only by station and category"""
    df_filtered = DF.copy()
    
    # Filter only by station and category, not year
    if station != 'Semua':
        df_filtered = df_filtered[df_filtered['stasiun'] == station]
    
    if category != 'Semua':
        df_filtered = df_filtered[df_filtered['categori'] == category]
    
    return create_category_trend(df_filtered)

def create_data_table(data):
    """Create interactive data table"""
    df = data
    
    if len(df) == 0:
        return pn.pane.Markdown("### Tidak ada data untuk ditampilkan")
    
    # Select relevant columns and format
    table_df = df[['tanggal', 'stasiun', 'categori', 'max', 'critical', 'pm25', 'pm10', 'so2', 'co', 'o3', 'no2']].copy()
    table_df = table_df.sort_values('tanggal', ascending=False)
    
    # Format tanggal column
    table_df['tanggal'] = table_df['tanggal'].dt.strftime('%Y-%m-%d')
    
    table = pn.widgets.Tabulator(
        table_df,
        page_size=20,
        pagination='remote',
        sizing_mode='stretch_width',
        theme='modern',
        show_index=False,
        layout='fit_data_table',
        height=600
    )
    
    return table

# Bind visualizations to filtered data
time_series_plot = pn.bind(create_time_series_plot, filtered_df)
category_chart = pn.bind(create_category_bar_chart, filtered_df)
station_chart = pn.bind(create_station_comparison, filtered_df)
monthly_heatmap = pn.bind(create_monthly_heatmap, filtered_df)
pollutant_pie = pn.bind(create_pollutant_pie_chart, filtered_df)
monthly_trend = pn.bind(create_monthly_trend, filtered_df)
pollutant_boxplot = pn.bind(create_pollutant_boxplot, filtered_df)
# Category trend uses all years, only filtered by station and category
category_trend_all = pn.bind(create_category_trend_all_years, station_filter, category_filter)
data_table = pn.bind(create_data_table, filtered_df)

# Dashboard Assembly
overview_tab = pn.Column(
    pn.pane.Markdown('## Ringkasan Data', margin=(0, 0, 10, 0)),
    summary_metrics,
    pn.pane.Markdown('### Tren ISPU Harian', margin=(15, 0, 5, 0)),
    time_series_plot,
    pn.pane.Markdown('### Distribusi Kategori', margin=(10, 0, 5, 0)),
    category_chart,
    pn.pane.Markdown('### Tren Kategori per Tahun', margin=(10, 0, 5, 0)),
    category_trend_all,
    sizing_mode='stretch_width'
)

analysis_tab = pn.Column(
    pn.pane.Markdown('## Analisis Pola', margin=(0, 0, 10, 0)),
    pn.pane.Markdown('### Pola Musiman (Heatmap)', margin=(5, 0, 5, 0)),
    monthly_heatmap,
    pn.Row(
        pn.Column(pn.pane.Markdown('### Tren Bulanan', margin=(10, 0, 5, 0)), monthly_trend),
        pn.Column(pn.pane.Markdown('### Polutan Kritis', margin=(10, 0, 5, 0)), pollutant_pie),
        sizing_mode='stretch_width'
    ),
    sizing_mode='stretch_width'
)

station_tab = pn.Column(
    pn.pane.Markdown('## Perbandingan Stasiun', margin=(0, 0, 10, 0)),
    pn.pane.Markdown('### Rata-rata Polutan per Stasiun', margin=(5, 0, 5, 0)),
    station_chart,
    pn.pane.Markdown('### Distribusi Polutan (Box Plot)', margin=(10, 0, 5, 0)),
    pollutant_boxplot,
    sizing_mode='stretch_width'
)

data_tab = pn.Column(
    pn.pane.Markdown('## Data Detail', margin=(0, 0, 10, 0)),
    data_table,
    sizing_mode='stretch_width'
)

tabs = pn.Tabs(
    ('Ringkasan', overview_tab),
    ('Analisis', analysis_tab),
    ('Stasiun', station_tab),
    ('Data', data_tab),
    sizing_mode='stretch_width'
)

template = pn.template.FastListTemplate(
    title='Dashboard Kualitas Udara Jakarta',
    sidebar=[
        pn.pane.HTML(
            '''<div style="padding: 12px; border-bottom: 1px solid #e0e0e0; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="ri-windy-line" style="font-size: 28px; color: #1976D2;"></i>
                    <div>
                        <div style="font-size: 15px; font-weight: 600; color: #333;">ISPU Monitor</div>
                        <div style="font-size: 11px; color: #666;">Jakarta Air Quality</div>
                    </div>
                </div>
            </div>'''
        ),
        pn.pane.Markdown('**Filter Data**', margin=(0, 5, 8, 5)),
        year_filter,
        station_filter,
        category_filter,
        pn.Spacer(height=15),
        pn.pane.HTML(
            '''<div style="padding: 10px; background: #f5f5f5; border-left: 3px solid #2196F3;">
                <div style="font-size: 12px; font-weight: 600; margin-bottom: 6px; color: #333;">
                    <i class="ri-information-line"></i> Tentang
                </div>
                <div style="font-size: 11px; line-height: 1.5; color: #666;">
                    Data kualitas udara Jakarta 2010-2025 dari 5 stasiun:<br>
                    <i class="ri-map-pin-line"></i> DKI1 (Bunderan HI)<br>
                    <i class="ri-map-pin-line"></i> DKI2 (Kelapa Gading)<br>
                    <i class="ri-map-pin-line"></i> DKI3 (Jagakarsa)<br>
                    <i class="ri-map-pin-line"></i> DKI4 (Lubang Buaya)<br>
                    <i class="ri-map-pin-line"></i> DKI5 (Kebon Jeruk)
                </div>
            </div>'''
        )
    ],
    main=[tabs],
    accent_base_color='#2196F3',
    header_background='#1976D2'
)

template.servable()
