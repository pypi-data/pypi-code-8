# Standard Library
import time
from contextlib import contextmanager

# Third Party Stuff
import splinter
from PIL import Image, ImageChops
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import staleness_of


@contextmanager
def wait_for_mathjax_loading(driver, timeout=30):

    javascript_code = '''
    MathJax.Hub.Register.StartupHook("End",
        function () {
            window.MathJaxSetupDone = true;
        }
    );
    return window.MathJaxSetupDone === true;
    '''.strip()

    yield
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script(javascript_code) is True
    )


def is_transparent(image):
    """
    Check to see if an image is transparent.
    """
    if not isinstance(image, Image.Image):
        # Can only deal with PIL images, fall back to the assumption that that
        # it's not transparent.
        return False
    return (image.mode in ('RGBA', 'LA') or
            (image.mode == 'P' and 'transparency' in image.info))


def webkit2png(url, image_file_path, browser=None, wait_time=0):
    new_browser = False
    try:
        if not browser:
            browser = splinter.Browser('phantomjs')
            new_browser = True
        browser.visit(url)
        if browser.status_code.is_success():
            if wait_time > 0:
                try:
                    with wait_for_mathjax_loading(browser.driver):
                        time.sleep(wait_time)
                except TimeoutException:
                    pass

            browser.driver.save_screenshot(image_file_path)
            image = Image.open(image_file_path)
            image.load()
            if is_transparent(image) and False:
                no_alpha = Image.new('L', image.size, (255))
                no_alpha.paste(image, mask=image.split()[-1])
            else:
                no_alpha = image.convert('L')
            # Convert to black and white imageage.
            bw = no_alpha.convert('L')
            # bw = bw.filter(ImageFilter.MedianFilter)
            # White background.
            bg = Image.new('L', image.size, 255)
            bbox = ImageChops.difference(bw, bg).getbbox()
            if bbox:
                image = image.crop(bbox)
            image.save(image_file_path)
    finally:
        if new_browser:
            browser.quit()
