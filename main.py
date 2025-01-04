# Selenium Imports
import os
import pathlib
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


from webdriver_manager.chrome import ChromeDriverManager

# Selenium Imports
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.core.driver_cache import DriverCacheManager

from contextlib import suppress


class RemoveSaveds:
    """
    A class to automate the removal of saved items on Facebook using Selenium WebDriver.
    Attributes
    ----------
    tries : int
        A counter to keep track of the number of attempts to remove saved items.
    Methods
    -------
    init() -> None:
        Initializes the Selenium WebDriver, sets up Chrome options, and starts the removal process.
    get_save(driver: WebDriver):
        Navigates to the Facebook saved items page.
    remove(driver: WebDriver):
        Attempts to remove saved items from the Facebook saved items page. Retries up to 3 times if items are not found.
    """

    def init(self) -> None:

        self.tries: int = 0
        chrome_options = Options()
        path_chrome = os.path.join(pathlib.Path(__file__).parent.resolve())

        os.makedirs("chrome", exist_ok=True)

        chrome_options.add_argument("--window-size=1600,900")
        chrome_options.add_argument(
            f"user-data-dir={os.path.join(path_chrome, "chrome")}"
        )

        driver_cache_manager = DriverCacheManager(root_dir=path_chrome)
        driverinst = ChromeDriverManager(cache_manager=driver_cache_manager).install()
        path = os.path.join(
            pathlib.Path(driverinst).parent.resolve(), "chromedriver.exe"
        )
        driver = webdriver.Chrome(service=Service(path), options=chrome_options)

        self.get_save(driver)
        self.remove(driver)

    def get_save(self, driver: WebDriver):

        driver.get("https://www.facebook.com/saved")

    def remove(self, driver: WebDriver):

        wait = WebDriverWait(driver, 10)

        try:

            sleep(0.5)
            items = None

            with suppress(NoSuchElementException, TimeoutException):
                items = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 'div[class="x1yztbdb"]')
                    )
                )

            if items and self.tries < 3:

                for item in items:

                    sleep(1)
                    more = item.find_elements(By.CSS_SELECTOR, 'div[class="x1emribx"]')[
                        -1
                    ]
                    more.click()

                    sleep(1)

                    remove_item = wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                'div[class="x1qjc9v5 x7sf2oe x78zum5 xdt5ytf x1n2onr6 x1al4vs7"]',
                            )
                        )
                    )
                    remove_item.click()

                sleep(1)
                self.remove(driver)

            elif not items:

                sleep(2)
                self.tries += 1

                self.get_save(driver)
                self.remove(driver)

        except Exception:
            sleep(1)

            self.tries += 1

            self.get_save(driver)
            self.remove(driver)


RemoveSaveds().init()
os.system("pause")
