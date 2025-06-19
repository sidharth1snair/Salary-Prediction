from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_jobs(keyword, num_jobs, verbose, slp_time):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.glassdoor.co.in/Job/data-scientist-jobs-SRCH_IN115_KO0,14.htm?sortBy=date_desc"
    driver.get(url)

    print("🌐 Website loaded. Expanding job list...")

    # Step 2: Keep clicking "Show more jobs" until enough are loaded
    while True:
        time.sleep(slp_time)

        try:
            driver.find_element(By.CLASS_NAME, "eigr9kq2").click()
        except (NoSuchElementException, ElementClickInterceptedException):
            pass
        try:
            driver.find_element(By.CLASS_NAME, "modal_closeIcon").click()
        except NoSuchElementException:
            pass

        job_cards = driver.find_elements(By.CSS_SELECTOR, 'li[class*="JobsList_jobListItem"]')
        print(f"🔎 Found {len(job_cards)} job cards")

        if len(job_cards) >= num_jobs:
            print("✅ Loaded enough jobs. Proceeding to scrape...")
            break

        # Scroll and try to click "Show more jobs"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        try:
            show_more_btn = driver.find_element(By.XPATH, '//button[@data-test="load-more"]')
            if show_more_btn.is_displayed():
                driver.execute_script("arguments[0].click();", show_more_btn)
                print("🟩 Clicked 'Show more jobs'")
                time.sleep(2)
        except NoSuchElementException:
            print("❌ 'Show more jobs' button not found — may have reached the end.")
            break

    # Step 3: Scrape job data
    jobs = []
    seen_jobs = set()
    job_cards = driver.find_elements(By.CSS_SELECTOR, 'li[class*="JobsList_jobListItem"]')

    print("📝 Scraping job details...")

    for job_card in job_cards:
        if len(jobs) >= num_jobs:
            break

        try:
            driver.execute_script("arguments[0].scrollIntoView();", job_card)
            job_card.click()
            time.sleep(2)

            job_title = driver.find_element(By.CSS_SELECTOR, 'h1[id^="jd-job-title"]').text

            try:
                company_name = driver.find_element(By.CSS_SELECTOR, "a[class*='EmployerProfile_profileContainer']").text
            except NoSuchElementException:
                try:
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

            job_id = (job_title, company_name, location)
            if job_id in seen_jobs:
                continue
            seen_jobs.add(job_id)

            if verbose:
                print(f"✅ {job_title} | {company_name} | {location} | {salary_estimate} | {rating}")

            jobs.append({
                "Job Title": job_title,
                "Company Name": company_name,
                "Location": location,
                "Salary Estimate": salary_estimate,
                "Rating": rating,
                "Job Description": job_description
            })

        except Exception as e:
            print("⚠️ Skipping job due to error:", e)
            continue

    driver.quit()
    return pd.DataFrame(jobs)


if __name__ == "__main__":
    keyword = "Data Scientist"
    num_jobs = 1500
    verbose = True
    slp_time = 1

    df = get_jobs(keyword, num_jobs, verbose, slp_time)
    df.to_csv("glassdoor_jobs_final.csv", index=False)
    print("\n📁 Saved scraped data to 'glassdoor_jobs_unique.csv'")
