import json
import os
import platform
import time
import urllib.request
from datetime import datetime
from io import BytesIO
from pathlib import Path
from random import randrange
from sys import stderr

from PIL import Image
from mastodon import Mastodon, MastodonAPIError, MastodonNetworkError
from selenium import webdriver

width = 1200
height = 1000

is_linux = platform.system() == 'Linux'
debug = os.getenv('DEBUG', False)

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
create mastodon API
"""
m_config = json.load(open('config.json', 'r'))

mast_api = Mastodon(
        client_id=m_config['client_key'],
        client_secret=m_config['client_secret'],
        api_base_url=m_config['client_host'],
        access_token=m_config['access_token'],
        debug_requests=False,
        request_timeout=15,
        ratelimit_method='throw'
)

media_ids = []

"""
Capture the site images
"""
date = datetime.now().strftime('%Y%m%d%H%M%S')
cap_folder = Path(f'caps/{date}')
cap_folder.mkdir()

for (name, url, b, q) in sites:
    print(name, url)
    driver.get(url)
    cap = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(cap))
    cap_path = f'{cap_folder}/{name}.png'
    im.save(cap_path)
    images.append(im)
    description = f"Front page of {name}\n"
    media_ids.append(mast_api.media_post(cap_path, description=description))

driver.quit()

if is_linux:
    display.stop()

"""
Combine the site images
"""
# w, h = images[0].size
#
# comp_image = Image.new('RGB', (w, h * 4))
#
# for i in range(4):
#     comp_image.paste(images[i], (0, (i * h)))
#
# comp_path = f'{cap_folder}/comp-{width}-{height}.jpg'
# comp_image.save(comp_path)

"""
Send toot
"""

if not debug:
    posted = False

    while not posted:
        try:
            # media_id = [mast_api.media_post(comp_path, description=description)]

            post = mast_api.status_post(
                    u"\u2063",
                    media_ids=media_ids,
                    visibility='private',
                    sensitive=False)

            posted = True

        except (MastodonAPIError, MastodonNetworkError) as e:
            print(e, file=stderr)
            time.sleep(15)

