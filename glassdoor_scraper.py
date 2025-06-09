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
    # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={keyword}"
    driver.get(url)
    jobs = []



    while len(jobs) < num_jobs:
        time.sleep(slp_time)

        # Close pop-ups if any
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

            # 🛡️ Handle sign-in popup again if it reappears
            try:
                driver.find_element(By.CLASS_NAME, "CloseButton").click()
                print("✅ Closed popup during job loop.")
            except NoSuchElementException:
                pass
            except Exception as e:
                print("⚠️ Popup close error mid-loop:", e)

            try:
                job_card.click()
                time.sleep(2)

        # Continue with scraping as before...


                job_title = driver.find_element(By.CSS_SELECTOR, 'h1[id^="jd-job-title"]').text
                company_name = driver.find_element(By.CSS_SELECTOR, "a[class*='EmployerProfile_profileContainer']").text
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
        time.sleep(3)

        # try:
        #     next_button = driver.find_element(By.XPATH, '//button[@data-test="pagination-next"]')
        #     if next_button.is_enabled():
        #         next_button.click()
        #     else:
        #         print("No more pages.")
        #         break
        # except NoSuchElementException:
        #     print("Next button not found.")
        #     break

    driver.quit()
    return pd.DataFrame(jobs)

if __name__ == "__main__":
    # Parameters
    keyword = "Data Scientist"
    num_jobs = 30
    verbose = True
    path = "C:/Users/sidha/Desktop/ds_salary_proj/chromedriver.exe"  # Update with the correct path on your system
    slp_time = 5  # Adjust based on your internet speed

    # Run scraper
    df = get_jobs(keyword, num_jobs, verbose, path, slp_time)

    # Save to CSV (optional)
    df.to_csv("glassdoor_jobs.csv", index=False)
    print("\nSaved scraped data to 'glassdoor_jobs.csv'")
