import geopandas
import pandas as pd
import re
from datetime import datetime
import matplotlib.pyplot as plt

# a list of latitudes and longtitudes of all ipv4 addresses
latitudes, longtitudes = [], []

# mapping ipv4 to [latitude, longtitude]
ip_coords_dict = {}

# mapping ipv4 to [h0, h1, h2, ..., hn] where 0 <= n <= 24
ip_hour_dict = {}

# Read in all the records "ip latitude longtitude" and 
# build up ip_coords_dict, latitudes, longtitudes
with open("coords.txt", 'r') as f:
  for line in f:
    ip, latitude, longtitude = line.split(' ')
    latitudes.append(latitude)
    longtitudes.append(longtitude)
    ip_coords_dict[ip] = [latitude, longtitude]
  f.close()

# regex of a valid ipv4 address
ptn_ipv4 = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

prog = re.compile(ptn_ipv4)

# Read in original csv file
logfilename = 'nasa_access_log_500k.csv'

print(f"reading file: {logfilename}")
df_all = pd.read_csv(logfilename, low_memory=False, parse_dates=['timestamp'])

# build up ip_hour_dict
for timestamp, location in zip(df_all['timestamp'], df_all['clientloc']):
  match_ipv4 = prog.match(location)
  if match_ipv4:
    if match_ipv4.string in ip_hour_dict:
      ip_hour_dict[match_ipv4.string].append(timestamp.hour)
    else:
      ip_hour_dict[match_ipv4.string] = [ timestamp.hour ]


def plot_on_map(latitudes: list, longtitudes: list, 
                title: str, color: str='green') -> None:
  """ Plot coords provided on world map
  """
  df = pd.DataFrame({
    'Latitude': latitudes,
    'Longitude': longtitudes
  })
  gdf   = geopandas.GeoDataFrame(df, 
                                 geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
  world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
  ax    = world.plot(color='white', edgecolor='black')

  gdf.plot(ax=ax, marker='.', color='green', markersize=10, alpha=0.5)
  plt.title(title)
  plt.show()


def plot_by_hours(start:int, end:int) -> None:
  """ Plot all coordinates based on "start" hour and "end" hour [start, end)
      If a whole day is to be plotted, start := 0, and end := 25
  """
  appeared_ips = set()
  for ip in ip_hour_dict:
    # check if hour is in range of [start, end), also check if ip actually
    # exists in ip_coords_dict (due to some ip cannot be queried successfully)
    if (all(hour >= start and hour < end for hour in ip_hour_dict[ip]) 
        and ip in ip_coords_dict):
      appeared_ips.add(ip)
  coords = list(zip(*[ip_coords_dict[coord] for coord in appeared_ips]))
  plot_on_map(coords[0], coords[1], 
          str(start) + ":00 to " + str(end - 1) + ":00 clients request")


plot_by_hours(0, 7)
plot_by_hours(7, 13)
plot_by_hours(13, 19)
plot_by_hours(19, 25)
