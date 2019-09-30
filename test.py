from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()

options = webdriver.FirefoxOptions()
options.add_argument('-headless')

driver = webdriver.Firefox(options=options)
driver.get('https://google.com')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print(driver.title)