from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def dummy():
    chrome_options = Options()
    chrome_options.add_argument("--headles")

    chrome_path = r'/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

    driver.get("http://google.com.ar/")
    print(driver.page_source)

    driver.quit()


if __name__ == '__main__':
    dummy()
