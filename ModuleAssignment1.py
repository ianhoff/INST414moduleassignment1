import pandas as pd
import folium
from folium.plugins import HeatMap
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

parking_data = pd.read_csv("Parking_Violations_Issued_in_April_2024.csv")
parking_data = parking_data.dropna(subset=['LATITUDE', 'LONGITUDE'])

datetime_data = []
for index, row in parking_data.iterrows():
    time = str(row['ISSUE_TIME'])
    date = row['ISSUE_DATE']
    
    dt = date + time.zfill(4)
    
    date_time = datetime.strptime(dt, "%Y/%m/%d %H%M")
    datetime_data.append(date_time)
    
parking_data['DATETIME'] = datetime_data
parking_data['HOUR'] = parking_data['DATETIME'].dt.hour
    
hour_counts = Counter(dt.hour for dt in datetime_data)

hours = []
counts = []
for hour, count in sorted(hour_counts.items()):
    hours.append(hour)
    counts.append(count)

def create_hourly_heatmap(df, hour):
    hour_df = df[df['HOUR'] == hour]
    heat_data = hour_df[['LATITUDE', 'LONGITUDE']].values.tolist()
    
    m = folium.Map(location=[38.9, -77.03], zoom_start=12)  # Center on DC
    HeatMap(heat_data, radius=10, blur=15, max_zoom=13).add_to(m)
    
    m.save(f"dc_violations_heatmap_hour_{hour}.html")
    return m



if __name__ == "__main__":
    for h in range(24):
        create_hourly_heatmap(parking_data, h)