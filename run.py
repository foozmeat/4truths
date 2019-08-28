import platform
from io import BytesIO
from pathlib import Path
from selenium import webdriver
from PIL import Image
import urllib.request

width = 1200
height = 1000

is_linux = platform.system() == 'Linux'

if is_linux:
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(width, height))
    display.start()

ublock_filename = 'ublock_origin-1.21.2-an+fx.xpi'
ublock = Path.joinpath(Path.cwd(), ublock_filename)
if not ublock.exists():
    print("Downloading uBlock")
    url = 'https://addons.mozilla.org/firefox/downloads/file/3361355/ublock_origin-1.21.2-an+fx.xpi'
    urllib.request.urlretrieve(url, ublock_filename)

profile = webdriver.FirefoxProfile()

profile.set_preference('font.minimum-size.x-western', 16)

driver = webdriver.Firefox(firefox_profile=profile)
driver.install_addon(ublock.as_posix(), temporary=False)

images = []

driver.get("https://nytimes.com")
print(driver.title)
images.append(driver.get_screenshot_as_png())

driver.get("https://www.washingtonpost.com/")
print(driver.title)
images.append(driver.get_screenshot_as_png())

driver.get("https://foxnews.com/")
print(driver.title)
images.append(driver.get_screenshot_as_png())

driver.get("https://cnn.com/")
print(driver.title)
images.append(driver.get_screenshot_as_png())

driver.quit()

if is_linux:
    display.stop()

im = Image.open(BytesIO(images[0]))
# im.save('caps/1.png')
w, h = im.size

comp_image = Image.new('RGB', (w, h*4))
comp_image.paste(im, (0, 0))

im = Image.open(BytesIO(images[1]))
# im.save('caps/2.png')
comp_image.paste(im, (0, h))

im = Image.open(BytesIO(images[2]))
# im.save('caps/3.png')
comp_image.paste(im, (0, h*2))

im = Image.open(BytesIO(images[3]))
# im.save('caps/4.png')
comp_image.paste(im, (0, h*3))

comp_image.save(f'caps/comp-{width}-{height}.jpg')

