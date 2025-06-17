from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    from selenium.webdriver.chrome.service import Service

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.glassdoor.co.in/Job/data-scientist-jobs-SRCH_IN115_KO0,14.htm?sortBy=date_desc"
    driver.get(url)
    jobs = []



    while len(jobs) < num_jobs:
        time.sleep(slp_time)

        try:
            driver.find_element(By.CLASS_NAME, "eigr9kq2").click()
        except ElementClickInterceptedException:
            pass
        except NoSuchElementException:
            pass

        try:
            driver.find_element(By.CLASS_NAME, "modal_closeIcon").click()
        except NoSuchElementException:
            pass

        job_cards = driver.find_elements(By.CSS_SELECTOR, 'li[class*="JobsList_jobListItem"]')
        print(f"Found {len(job_cards)} job cards")

        for job_card in job_cards:
            if len(jobs) >= num_jobs:
                break

            try:
                driver.find_element(By.CLASS_NAME, "CloseButton").click()
                print("✅ Closed popup during job loop.")
            except NoSuchElementException:
                pass
            except Exception as e:
                print("⚠️ Popup close error mid-loop:", e)

            try:
                job_card.click()
                time.sleep(3)


                job_title = driver.find_element(By.CSS_SELECTOR, 'h1[id^="jd-job-title"]').text
                try:
                    company_name = driver.find_element(By.CSS_SELECTOR, "a[class*='EmployerProfile_profileContainer']").text
                except NoSuchElementException:
                    try:
                        # Sometimes it's just plain text in a <span> or <div>
                        company_name = driver.find_element(By.CSS_SELECTOR, "div[data-test='employerName']").text
                    except NoSuchElementException:
                        company_name = "N/A"
                location = driver.find_element(By.CSS_SELECTOR, '[data-test="location"]').text

                try:
                    salary_estimate = driver.find_element(By.CLASS_NAME, "SalaryEstimate_salaryRange__brHFy").text
                except NoSuchElementException:
                    salary_estimate = "N/A"

                try:
                    job_description = driver.find_element(By.CSS_SELECTOR, 'div[data-test="jobDescriptionContent"]').text
                except NoSuchElementException:
                    job_description = "N/A"

                try:
                    rating = driver.find_element(By.ID, "rating-headline").text
                except NoSuchElementException:
                    rating = "N/A"

                if verbose:
                    print(f"{job_title} | {company_name} | {location} | {salary_estimate} | {rating}")

                jobs.append({
                    "Job Title": job_title,
                    "Company Name": company_name,
                    "Location": location,
                    "Salary Estimate": salary_estimate,
                    "Rating": rating,
                    "Job Description": job_description
                })

            except Exception as e:
                print("Skipping job due to error:", e)
                continue

        # Scroll to load more jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("🔄 Scrolled to load more jobs...")
        time.sleep(2)


    driver.quit()
    return pd.DataFrame(jobs)

if __name__ == "__main__":
    # Parameters
    keyword = "Data Scientist"
    num_jobs = 500
    verbose = True
    path = "C:/Users/sidha/Desktop/ds_salary_proj/chromedriver.exe"  
    slp_time = 1  # Adjust based on your internet speed

    # Run scraper
    df = get_jobs(keyword, num_jobs, verbose, path, slp_time)

    # Save to CSV 
    df.to_csv("glassdoor_jobs.csv", index=False)
    print("\nSaved scraped data to 'glassdoor_jobs_date_desc.csv'")
