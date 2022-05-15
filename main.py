############################################## SETUP ##############################################

from time import sleep

from database import update_db, parse_data

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from multiprocessing import Pool

def main(start):

############################################## FUNCTION DEFINITIONS ##############################################


    #function to collect data (attribute) from web element given xpath
    def get_data(xpath,attr):
            try:
                return getattr(driver.find_element(By.XPATH, xpath),attr)
            except NoSuchElementException:
                pass
    #similar to above function but specifically for links (they're a bit wonky)
    def get_link():
            #check for external posting href
            try:
                job_link = driver.find_element(By.XPATH, external_link_xpath).get_attribute("href")
            #check for internal posting href
            except:
                try:
                    job_link = driver.find_element(By.XPATH, internal_link_xpath).get_attribute("data-indeed-apply-joburl")
                except:
                    job_link = "None"
            return job_link


############################################## VARIABLE DEFINITIONS ##############################################

    where = ["Houston%20TX","Austin%20TX"]

    for place in where:
        #set driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        #set driver wait
        wait = WebDriverWait

        #XPATHS
        jobs_xpath = "//td[@CLASS='resultContent']/div/h2/a"
        frame_xpath = "//*[@id='vjs-container-iframe']"
        root_xpath = "//*[@id='viewJobSSRRoot']"
        title_xpath = root_xpath+"//h1"
        employer_xpath = root_xpath+"//div[contains(@class, 'icl-u-lg-mr--sm icl-u-xs-mr--xs')]/a"
        location_xpath = root_xpath+"//div[contains(@class, 'JobInfoHeader-subtitle')]/div[2]/div"
        description_xpath = "//*[@id='jobDescriptionText']"
        external_link_xpath = "//*[@id='applyButtonLinkContainer']/div[1]/div[1]/a"
        internal_link_xpath = "//*[@id='jobsearch-ViewJobButtons-container']//*[contains(@class,'indeed-apply-widget')]"

        #JS code
        scroll_bot = "window.scrollTo(0, document.body.scrollHeight);"
        scroll_top = "window.scrollTo(0, 0);"

        #input vars
        what = "Software"

    ############################################## START OF PROCESSING ##############################################

        #load Indeed webpage
        print("LOADING WEBPAGE...")
        driver.get(f"https://www.indeed.com/jobs?q={what}&l={place}&start={start}")
        #Check search success
        assert "No results found." not in driver.page_source

        #scroll page to load all list items
        driver.execute_script(scroll_bot)
        driver.execute_script(scroll_top)
        sleep(2)

        #collect list of job postings (should be 15 per page)
        job_list = driver.find_elements(By.XPATH, jobs_xpath)

        #click each post, collect data from resulting iframe
        print("COLLECTING DATA...")
        for item in job_list:
            item.click()
            sleep(1)
            #switch to iframe
            wait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, frame_xpath)))
            #collect data
            job_title = get_data(title_xpath, "text")
            job_employer = get_data(employer_xpath, "text")
            job_location = get_data(location_xpath, "text")
            job_description = get_data(description_xpath, "text")
            job_link = get_link()
            print(job_link)
            #parse data
            job_lang, job_exp_req = parse_data(job_description)
            #update database
            update_db(job_title, job_employer, job_location, job_lang, job_exp_req,job_link)
            #switch back to base site before looping
            driver.switch_to.default_content()



############################################## PARALLEL RUNTIME ##############################################

#WARNING! DO NOT SET THE Pool(x) INPUT TOO HIGH OR YOU WILL BE FLAGGED AS A BOT
#THEY WILL MAKE YOU DO CAPTCHAS
#CAPTCHAS SUCK

start = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
if __name__ == '__main__':
    with Pool(4) as pool: 
        results = pool.map(main, start)
