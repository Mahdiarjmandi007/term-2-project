import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
wait = WebDriverWait(driver, 15)

driver.get("https://www.linkedin.com/login")

username = wait.until(EC.presence_of_element_located((By.ID, "username")))
username.send_keys("arjmandipython@gmail.com")  

password = wait.until(EC.presence_of_element_located((By.ID, "password")))
password.send_keys("user1234")  
password.send_keys(Keys.RETURN)


wait.until(EC.url_contains("feed"))
time.sleep(2)


with open("linkedin_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("✅ cookies has saved")

driver.quit()
