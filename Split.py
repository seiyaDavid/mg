import pandas as pd
import os

# Assuming 'df' is your DataFrame and 'Name' is the column to split on

# Create a directory to store the output files (optional)
output_dir = "split_by_name"
os.makedirs(output_dir, exist_ok=True)

# Group by 'Name' and save each group
for name, group in df.groupby('Name'):
    # Sanitize the name for file system safety
    safe_name = str(name).strip().replace(" ", "_").replace("/", "_")
    file_path = os.path.join(output_dir, f"{safe_name}.csv")
    group.to_csv(file_path, index=False)
