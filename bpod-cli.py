#!/usr/bin/python

"""
Python script to set bing image of the day as desktop wallpaper. Based on work by Anurag Rana.
OS: Ubuntu 21.04
GNOME: 3.38
Original Author: Anurag Rana
More Info: https://www.pythoncircle.com
"""

"""
LICENCE

Copyright 2020 Anurag Rana
Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in the 
Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
OR OTHER DEALINGS IN THE SOFTWARE.

"""

import datetime
import json
import os
from pathlib import Path
import requests

today = datetime.date.today().strftime("%Y-%m-%d")
CACHEDIR = os.path.join(os.path.expanduser('~'), '.local/share/bpod/cache/')

# get image url
def getImageUrl():
    response = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
    image_data = json.loads(response.text)
    image_url = image_data["images"][0]["url"]
    image_url = image_url.split("&")[0]
    return "https://www.bing.com" + image_url

# get image name
def getImageName(tstamp, imageUrl):
    image_name = imageUrl.split(".")[-2:]
    return today + "." + image_name[1]

# Check for the Cache directory, and create it if it doesn't exist
'''
ToDo:
[ ] Check the mode if the directory already exists
'''
def checkCache(cdir):
    if os.path.exists(cdir):
        pass
    else:
        os.makedirs(cdir, mode = 0o700)
    return

# download and save image
"""
ToDo:
[ ] Save to a named cache directory in your home directory
[ ] Scan the downloaded file for viruses
[ ] Manage the local cache to either delete the image daily or mange the size of the cache
"""
image_url = getImageUrl()
image_name = getImageName(today, image_url)
cache_file = os.path.join(CACHEDIR, image_name)
checkCache(CACHEDIR)
img_data = requests.get(image_url).content
with open(cache_file, 'wb') as handler:
    handler.write(img_data)

# ubuntu command to set wallpaper
command = "gsettings set org.gnome.desktop.background picture-uri 'file://" + cache_file + "'"
print(command)
os.system(command)
