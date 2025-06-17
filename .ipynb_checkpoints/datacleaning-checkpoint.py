import pandas as pd

# Load your CSV or DataFrame
df = pd.read_csv("glassdoor_jobs.csv")  # Replace with your actual file path

# Remove rows where 'Salary Estimate' is 'N/A'
df_cleaned = df[df['Salary Estimate'].notna()]  # Removes NaN
df_cleaned = df_cleaned[df_cleaned['Salary Estimate'] != 'N/A']  # Removes literal 'N/A'

# Optionally, reset the index
df_cleaned.reset_index(drop=True, inplace=True)

# Save the cleaned data
df_cleaned.to_csv("cleaned_file.csv", index=False)
