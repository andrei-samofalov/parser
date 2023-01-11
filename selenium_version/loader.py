from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')

browser = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
