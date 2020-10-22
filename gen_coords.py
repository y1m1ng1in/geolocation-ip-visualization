import ipinfo
import re
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

token = 'replace-me' 

handler = ipinfo.getHandler(token)

logfilename = 'nasa_access_log_500k.csv'

ptn_ipv4 = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

prog = re.compile(ptn_ipv4)

print(f"reading file: {logfilename}")

df = pd.read_csv(logfilename, low_memory=False, parse_dates=['timestamp'])

locations = df['clientloc']

ipv4s, hostnames = set(), set()

for loc in locations:
  match_ipv4 = prog.match(loc)
  if match_ipv4:
    ipv4s.add(match_ipv4.string)
  else:
    hostnames.add(loc)

coord_list = []
with open("coords.txt", 'w') as f:
  for ipv4 in ipv4s:
    try:
      coord = handler.getDetails(ipv4).loc.split(',')
      coord_list.append([float(coord[0]), float(coord[1])])
      f.write(ipv4 + ' ' + coord[0] + ' ' + coord[1] + '\n')
    except Exception:
      pass
    finally:
      pass
  f.close()
