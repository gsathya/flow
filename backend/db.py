import sqlite3
import pygeoip
import json

def is_private(address):
  """
  Checks if the IPv4 address is in a range belonging to the local network or
  loopback. These include:

    * Private ranges: 10.*, 172.16.* - 172.31.*, 192.168.*
    * Loopback: 127.*
  """

  # checks for any of the simple wildcard ranges
  if address.startswith("10.") or address.startswith("192.168.") or address.startswith("127."):
    return True

  # checks for the 172.16.* - 172.31.* range
  if address.startswith("172."):
    second_octet = int(address.split('.')[1])

    if second_octet >= 16 and second_octet <= 31:
      return True

  return False

def process_db():
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    conn = sqlite3.connect('traceroute-data.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("SELECT * FROM traceroute LIMIT 100")

    rows = cur.fetchall()

    paths = []
    path = []
    dest = None
    
    for row in rows:
        # new path
        if row["hop"] == 1:
            # add prev path to our list
            if path:
                # dest should be added at the end
                if dest and path[-1] != dest:
                    path.append(dest)
                    dest = None

                paths.append(path)
            ip_info = gi.record_by_addr(row["srcip"])
            path = [(ip_info["latitude"], ip_info["longitude"])]

        ip = row["ip"]

        if is_private(ip) or ip == "*":
            continue

        ip_info = gi.record_by_addr(ip)
        lat, lang = ip_info["latitude"], ip_info["longitude"]

        if path[-1] != (lat, lang):
            path.append((lat, lang))

        if not dest:
            ip_info = gi.record_by_addr(ip)
            lat, lang = ip_info["latitude"], ip_info["longitude"]
            dest = (lat, lang)

    # add final path that we missed
    if path:
        if dest and path[-1] != dest:
            path.append(dest)
        paths.append(path)

    with open("data.json", 'w') as fh:
        data = {'paths': paths}
        json.dump(data, fh)

    print data
    conn.close()

if __name__ == "__main__":
    process_db()
