#!/usr/bin/env python

from datetime import datetime
from hashlib import md5
import os.path
import sys

import requests


target_dir = os.path.abspath("./zipcode_coordinates/data")

# fetch latest zip code coordinates
coordinates = {}
limit = 100
offset = 0
while True:
    print(f"› Fetching records {offset+1} to {offset+limit}")
    url = f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-germany-postleitzahl/records?select=plz_code%2Cgeo_point_2d&limit={limit}&offset={offset}"  # noqa: E501
    r = requests.get(url)
    assert r.status_code == 200
    data = r.json()
    for row in data["results"]:
        coordinates[row["plz_code"]] = (
            row["geo_point_2d"]["lat"],
            row["geo_point_2d"]["lon"],
        )
    if len(data["results"]) < limit:
        break
    offset += limit

# compare previous hash with new hash
hash_file_name = os.path.join(target_dir, "de.md5")
previous_hash = open(hash_file_name).read().strip()
new_hash = md5(r.content).hexdigest()
if new_hash == previous_hash:
    print("No new data")
    sys.exit(0)
print("New data available")

# write new hash
with open(hash_file_name, "w") as f:
    f.write(new_hash)

# write new data
with open(os.path.join(target_dir, "de.py"), "w") as f:
    f.write("coordinates = %s\n" % (coordinates,))

# write new version
now = datetime.now()
version = now.strftime("%Y%m%d")
print(f"New version: {version}")
with open("./zipcode_coordinates/version.py", "w") as f:
    f.write(f'last_update = "{version}"\n')
