#!/usr/bin/env python

from datetime import datetime
from hashlib import md5
import io
import os.path
import urllib.request
import zipfile


target_dir = os.path.abspath("./zipcode_coordinates/data")
create_new_version = False

# fetch latest zip code coordinates from geonames.org
for isocode in ["DE", "AT", "CH"]:
    print(isocode, end=" › ")
    r = urllib.request.urlopen(f"http://download.geonames.org/export/zip/{isocode}.zip")
    assert r.status == 200
    z = zipfile.ZipFile(io.BytesIO(r.read()))
    data = {}
    hash_file_name = os.path.join(target_dir, f"{isocode}.md5")
    old_hash = open(hash_file_name).read().strip()

    with z.open(f"{isocode}.txt") as f:
        contents = f.read()
        new_hash = md5(contents).hexdigest()
        if new_hash == old_hash:
            print("No new data")
            continue

        print("New data available")

        f.seek(0)
        for line in f.readlines():
            row = line.decode("utf-8").strip().split("\t")
            data[row[1]] = (row[9], row[10])
        print(data)

    with open(hash_file_name, "w") as f:
        f.write(new_hash)

    with open(os.path.join(target_dir, f"{isocode}.py"), "w") as f:
        f.write("coordinates = %s\n" % (data,))

    create_new_version = True

if create_new_version:
    now = datetime.now()
    version = "{}.{}".format(now.strftime("%Y%m%d"), (now.hour * 60 + now.minute))
    print(f"New version: {version}")
    with open("./zipcode_coordinates/__init__.py", "w") as f:
        f.write(f'__version__ = "{version}"\n')
else:
    print("Data has not changed, no new version")
