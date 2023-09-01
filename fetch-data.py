#!/usr/bin/env python

from datetime import datetime
import io
import os.path
import urllib.request
import zipfile


# fetch latest zip code coordinates from geonames.org
r = urllib.request.urlopen("http://download.geonames.org/export/zip/DE.zip")
assert r.status == 200
z = zipfile.ZipFile(io.BytesIO(r.read()))
data = {}
with z.open("DE.txt") as f:
    for line in f.readlines():
        row = line.decode("utf-8").strip().split("\t")
        data[row[1]] = (row[9], row[10])

now = datetime.now()
version = "{}.{}".format(now.strftime("%Y%m%d"), (now.hour * 60 + now.minute))
with open("./zipcode_coordinates/__init__.py", "w") as f:
    f.write(f'__version__ = "{version}"\n')

target_dir = os.path.abspath("./zipcode_coordinates/data")
with open(os.path.join(target_dir, "DE.py"), "w") as f:
    f.write("coordinates = %s\n" % (data,))
