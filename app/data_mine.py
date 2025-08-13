from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import csv
import pickle
import sqlite3


class DT_MINE():
    def __init__(self):
        self.result=[]
        self.state="run"
        service = FirefoxService(executable_path="geckodriver.exe",port=5555)
        options = FirefoxOptions()
        self.driver = webdriver.Firefox(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)
    def login(self):
        
        self.driver.get("https://www.linkedin.com")
        time.sleep(2)

        try:
            with open("linkedin_cookies.pkl", "rb") as f:
                cookies = pickle.load(f)

            for cookie in cookies:
                if 'sameSite' in cookie:
                    if cookie['sameSite'] == 'None':
                        cookie['sameSite'] = 'Strict'
                self.driver.add_cookie(cookie)

            self.driver.refresh()

            self.wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))
            print("login was successful")

        except Exception as e:
            print("❌ error for login with cookies", e)
        
        
    def searching(self,job_tittle,location):
        self.driver.get("https://www.linkedin.com/jobs")
    
        what_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
        what_input.clear()
        what_input.send_keys(job_tittle)
        time.sleep(1)

        where_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")))
        where_input.clear()
        where_input.send_keys(location)
        time.sleep(1)

        where_input.send_keys(Keys.DOWN)
        where_input.send_keys(Keys.RETURN)
        time.sleep(1)

        what_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
        what_input.send_keys(Keys.RETURN)
        time.sleep(1)
    
    def data(self):
        jobs = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")
        ))
        list_of_jobs=[]
        seen_titles = set()
        index=0
        #scroll_container = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "div.jobs-search-results-list")))
        time.sleep(5)
        number_job=1
        while len(list_of_jobs)<20:
            
            jobs = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")
        ))
            try :
                job=jobs[index]
            except IndexError:
                print(f"errored jobs done or something happening")
                
                break


            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", job)
                time.sleep(1)

                title = job.find_element(By.CSS_SELECTOR, "a.job-card-container__link").get_attribute("aria-label")
                if title in seen_titles:
                    index+=1
                    continue
                seen_titles.add(title)

                company = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle").text
                location = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__caption").text
                link = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link").get_attribute("href")

                loc, type_ = location.split("(")
                type_ = type_[:-1]

                list_of_jobs.append([title, company, loc.strip(), type_.strip(), link])
                index+=1
                self.driver.execute_script("window.scrollBy(0, 150);")
                time.sleep(1)
                print("job",number_job,": success full")
                number_job+=1

            except Exception as e:
                print(e)
                continue

        with open("jobs.csv", mode="w", encoding="utf-8-sig", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Name of Company", "Location", "Type", "Link"])
            writer.writerows(list_of_jobs)
        

        self.driver.quit()
        
        """
        for job in jobs[:10]:
            try:
                jobs = self.wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//li[contains(@class, 'occludable-update') and contains(@class, 'scaffold-layout__list-item')]")))
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
            writer.writerow(["Title","Name of Company","Location","Type","Link"])
            writer.writerows(list_of_jobs)"""
    def create_DB(self):
        connect=sqlite3.connect("job_DataBase.db")
        cursor=connect.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS tablejob (
                       Title TEXT,
                       Name_OF_Company TEXT,
                       Location TEXT,
                       Type TEXT,
                       Link TEXT
)                     
""")
        with open("jobs.csv" , newline="" ,encoding="utf-8") as csvfile:
            reader=csv.reader(csvfile)
            next(reader)
            for row in reader :
                cursor.execute("INSERT INTO tablejob (Title,Name_OF_Company,Location,Type,Link) VALUES (?,?,?,?,?)",row)
        connect.commit()
        connect.close()

        

    def run(self,job,location):
        self.status="No"
        self.job=job
        self.location=location
        self.login()
        self.searching(job,location)
        self.data()
        self.create_DB()
        



