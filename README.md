

# Salary Prediction Using Machine Learning

This project predicts job salaries using machine learning models trained on data scraped from Glassdoor. It includes job scraping automation, data cleaning, feature engineering, visual exploration, multiple regression models, and ensemble learning for optimal performance.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Results](#results)


---

## Overview

Accurately estimating salaries is crucial for candidates and employers. This project automates the extraction of job data from Glassdoor and builds a regression model to predict average salaries based on job title, company, location, rating, etc.

---

## Features

-  Automated scraping of job listings using Selenium
-  Cleans and standardizes messy real-world job data
-  Visualizes salary trends by location, role, and range
-  Trains multiple ML models: Linear, Lasso, Random Forest
-  Uses hyperparameter tuning for optimization
-  Final prediction via ensemble (Voting Regressor)

---

## Tech Stack

- **Language**: Python 3.11+
- **Libraries**:
  - `pandas`, `numpy`
  - `matplotlib`, `seaborn`
  - `scikit-learn`
  - `selenium`, `webdriver-manager`
- **Tools**: Jupyter Notebook, ChromeDriver

---

## Project Structure
<pre>
Salary-Prediction/
│
├── data/
│ ├── glassdoor_jobs_raw.csv
│ └── glassdoor_cleaned_new.csv
│
├── notebooks/
│ ├── 01_scraping_jobs.ipynb
│ ├── 02_cleaning_salary_data.ipynb
│ ├── 03_eda_and_visualizations.ipynb
│ └── 04_modeling_and_prediction.ipynb
│
├── scripts/
│ └── scraper.py
│
|
├── requirements.txt
└── README.md
 </pre>


 

## How to Run

### 1. Clone the repository

```
git clone https://github.com/sidharth1snair/Salary-Prediction.git
cd Salary-Prediction
```
### 2. Install dependencies

```
pip install -r requirements.txt

```
### 3. Run Jupyter notebooks
Open each .ipynb notebook in order:

#### 1. scraping_jobs.py — Scrape and save job listings

#### 2. cleaning_salary_data.ipynb — Clean, extract salary info, generalize roles

#### 3. eda_and_visualizations.ipynb — Plot salary trends, distributions, and insights

#### 4. modeling_and_prediction.ipynb — Train ML models and evaluate
