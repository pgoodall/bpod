#!/usr/bin/python3

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
import subprocess
from pathlib import Path
from sys import stdout
import requests

today = datetime.date.today().strftime("%Y-%m-%d")
cache_dir = os.path.join(os.path.expanduser('~'), '.local/share/bpod/cache/')
current_bg_file = subprocess.check_output(["gsettings", "get", "org.gnome.desktop.background", "picture-uri"], text=True)

# get image url
def get_image_url():
    response = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
    image_data = json.loads(response.text)
    image_url = image_data["images"][0]["url"]
    image_url = image_url.split("&")[0]
    return "https://www.bing.com" + image_url

# get image name
def get_image_name(tstamp, imageUrl):
    image_name = imageUrl.split(".")[-2:]
    return today + "." + image_name[1]

# Check for the Cache directory, and create it if it doesn't exist
def check_cache(cdir):
    if os.path.exists(cdir):
        pass
    else:
        os.makedirs(cdir, mode = 0o700)
    return

# Set background on Ubuntu
def set_background_ubuntu(new_bg):
    command = "gsettings set org.gnome.desktop.background picture-uri 'file://" + new_bg + "'"
    print("Applying new background image...")
    os.system(command)


# Check if they want to keep the new background or restore the previous background
def check_for_save(previous_bg):
    command = "gsettings set org.gnome.desktop.background picture-uri " + previous_bg
    keep_prompt = input("Keep the new background? (y/n): ")
    if keep_prompt == 'n':
        print("Restoring previous background...")
        print(command)
        os.system(command)



# download and save image
image_url = get_image_url()
image_name = get_image_name(today, image_url)
cache_file = os.path.join(cache_dir, image_name)
check_cache(cache_dir)
img_data = requests.get(image_url).content
with open(cache_file, 'wb') as handler:
    handler.write(img_data)

set_background_ubuntu(cache_file)
check_for_save(current_bg_file)
