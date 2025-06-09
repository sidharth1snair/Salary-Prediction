from glassdoor_scraper import get_jobs
import pandas as pd

if __name__ == "__main__":
    df = get_jobs(keyword='data scientist', num_jobs=15, verbose=True)
    if not df.empty:
        df.to_csv("glassdoor_jobs.csv", index=False)
        print("✅ Data saved to 'glassdoor_jobs.csv'")
    else:
        print("❌ No jobs collected.")
