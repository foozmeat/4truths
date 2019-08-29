import json
import platform
from io import BytesIO
from pathlib import Path
from random import randrange

from selenium import webdriver
from PIL import Image
import urllib.request
import csv

width = 1200
height = 1000

is_linux = platform.system() == 'Linux'

"""
Download uBlock
"""
ublock_filename = 'ublock_origin-1.21.2-an+fx.xpi'
ublock = Path.joinpath(Path.cwd(), ublock_filename)
if not ublock.exists():
    print("Downloading uBlock")
    url = 'https://addons.mozilla.org/firefox/downloads/file/3361355/ublock_origin-1.21.2-an+fx.xpi'
    urllib.request.urlretrieve(url, ublock_filename)

"""
Start up the virtual framebuffer if we're on Linux
"""
if is_linux:
    from pyvirtualdisplay import Display

    display = Display(visible=0, size=(width, height))
    display.start()

"""
Load Site data
"""

buckets = json.load(open('sites.json', 'r'))
sites = []
for site_i in range(4):
    n = randrange(len(buckets[site_i]))
    sites.append(buckets[site_i][n])

"""
Start Firefox and bump up the font size
"""
profile = webdriver.FirefoxProfile()
profile.set_preference('font.minimum-size.x-western', 16)
driver = webdriver.Firefox(firefox_profile=profile)
driver.install_addon(ublock.as_posix(), temporary=False)

images = []
description = "Front pages of\n"

"""
Capture the site images
"""
for (name, url, b, q) in sites:
    print(name, url)
    driver.get(url)
    cap = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(cap))
    im.save(f'caps/{name}.png')
    images.append(im)
    description += f"{name}\n"

driver.quit()

print(description)

if is_linux:
    display.stop()

"""
Combine the site images
"""
w, h = images[0].size

comp_image = Image.new('RGB', (w, h * 4))

for i in range(4):
    comp_image.paste(images[i], (0, (i * h)))

comp_image.save(f'caps/comp-{width}-{height}.jpg')
