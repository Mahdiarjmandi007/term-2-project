from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
class DT_MINE():
    def __init__(self):
        self.result=[]
        self.driver=webdriver.Firefox()
    def login(self):
        
        
        self.driver.get("https://www.linkedin.com/login")

        username=self.driver.find_element(By.ID,"username")
        username.send_keys("arjmandipython@gmail.com")
        time.sleep(5)
        password=self.driver.find_element(By.ID, "password")
        password.send_keys("user1234")
        password.send_keys(Keys.RETURN)
        time.sleep(5)
    def searching(self,job_tittle,location):
        self.driver.get("https://www.linkedin.com/jobs")
    
        what_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")
        what_input.clear()
        what_input.send_keys(job_tittle)
        time.sleep(1)

        where_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")
        where_input.clear()
        where_input.send_keys(location)
        time.sleep(1)

        where_input.send_keys(Keys.DOWN)
        where_input.send_keys(Keys.RETURN)
        time.sleep(1)

        what_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")
        what_input.send_keys(Keys.RETURN)
        time.sleep(5)
    def data(self):
        jobs = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")
        list_of_jobs=[]
        for job in jobs[:10]:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", job)
                time.sleep(1)
                my_list=[]
                title= WebDriverWait(job, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.job-card-list__title--link"))).get_attribute("aria-label")
                my_list.append(title)
                company = WebDriverWait(job, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,"div.artdeco-entity-lockup__subtitle"))).text
                my_list.append(company)
                location = WebDriverWait(job, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,"div.artdeco-entity-lockup__caption"))).text
                link= WebDriverWait(job, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.job-card-list__title--link"))).get_attribute("href")
                
                loc,type=location.split("(")
                type=type[:-1]
                my_list.append(loc)
                my_list.append(type)
                my_list.append(link)
                list_of_jobs.append(my_list)
            
            except Exception as e:
                pass
        with open ("jobs.csv",mode="w",encoding="utf-8-sig",newline='') as file:
            writer=csv.writer(file)
            writer.writerow(["Titel","Name of Company","Location","Type","Link"])
            writer.writerows(list_of_jobs)


