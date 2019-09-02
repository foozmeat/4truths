import json
import os
import platform
import sys
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
height = 1200

is_linux = platform.system() == 'Linux'
debug = os.getenv('DEBUG', False)
nopost = os.getenv('NOPOST', False)

m_config = json.load(open('config.json', 'r'))

if m_config.get('sentry_url') and not debug:
    import sentry_sdk
    sentry_sdk.init(m_config.get('sentry_url'))

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

mast_api = Mastodon(
        client_id=m_config['client_key'],
        client_secret=m_config['client_secret'],
        api_base_url=m_config['client_host'],
        access_token=m_config['access_token'],
        debug_requests=False,
        request_timeout=15
)

media_ids = []
now = datetime.now()
post_body = ""

"""
Capture the site images
"""
date = now.strftime('%Y%m%d%H%M%S')
cap_folder = Path(f'caps/{date}')
cap_folder.mkdir()

for (name, url, b, q) in sites:
    if debug:
        print(name, url, b, q)
    driver.get(url)
    cap = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(cap))
    cap_path = f'{cap_folder}/{name}.png'
    im.save(cap_path)
    images.append(im)
    description = f"Front page of {name}\n"
    post_body += f"{name}\n"

    media_posted = False
    while not media_posted:
        try:
            if debug:
                print(f"posting image for {name}")
            if not nopost:
                media_ids.append(mast_api.media_post(cap_path, description=description))
            media_posted = True

        except MastodonNetworkError as e:
            print(e, file=sys.stderr)
            time.sleep(15)

driver.quit()

if is_linux:
    display.stop()

"""
Send toot
"""

posted = False

while not posted:
    try:

        if debug:
            print(post_body)

        if not nopost:
            nopost = mast_api.status_post(
                    post_body,
                    media_ids=media_ids,
                    sensitive=False)

        posted = True

    except (MastodonAPIError, MastodonNetworkError) as e:
        print(e, file=stderr)
        time.sleep(15)

