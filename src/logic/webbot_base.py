import sys

import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from user_agent import generate_user_agent
from webdriver_manager.chrome import ChromeDriverManager


class Connector:

    """Class Connector can be considered as the crawling engine instance initialization.
    Attributes:
        driver: the interactive web crawling engine. Can be either from package Selenium or SeleniumWire
    Methods:
        get_product_content_page_from_url: Entrance point of parsing an html page source code by BeautifulSoup into an html DOM
        get_bs4_page_content_tags: Parse the webpage currently visited by driver into an HTML DOM by BeautifulSoup.
    """

    def __init__(self, headless: bool = False, turn_off_image: bool = False):

        """
        Args:
            headless: if runs Chrome in headless mode.
            turn_off_image: if turn off showing images
        """

        self.__headless = headless
        self.default_page_load_timeout = 30
        self.__chrome_initialization(turn_off_image=turn_off_image)
        self.__retry = 0

    def __chrome_initialization(self, turn_off_image: bool):

        """
        Launch the interactive web crawling engine
        Args:
            turn_off_image: if turn off showing images
        """

        chrome_options = webdriver.ChromeOptions()
        if self.__headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")

        # User a randomly generated user agent
        if sys.platform == 'win32':
            operating_system = 'win'
        elif sys.platform == 'darwin':
            operating_system = 'mac'
        else:
            operating_system = 'linux'
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        user_agent = generate_user_agent(os=operating_system, navigator='chrome')

        chrome_options.add_argument(f"--user-agent=%s" % user_agent)

        prefs = {"translate_whitelists": {"your native language": "zh-TW"},
                 "translate": {"enabled": "True"}}

        # disable image and javascript loading
        if turn_off_image:
            prefs.update({
                'profile.default_content_setting_values': {
                    'images': 2,
                    'javascript': 2
                }
            })
            chrome_options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.driver.set_page_load_timeout(self.default_page_load_timeout)  # set page load timeout to 60 seconds

    def get_bs4_page_html(self) -> bs4.element.Tag:

        """
        parsing html DOM with BeautifulSoup
        Returns:
            DOM derived from web page source code parsed by BeautifulSoup
        """

        return BeautifulSoup(self.driver.page_source, "html.parser")
