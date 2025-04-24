import pandas as pd
import re
import os
import tempfile
import shutil
import sys
import numpy as np


def extract_code(name):
    """Extract the code from the name by finding the first word."""
    match = re.search(r"^(\w+)", name)
    return match.group(1) if match else ""


def process_files(input_file, lookup_file, name_column="Name", report_column="report"):
    # Read the lookup file into a dictionary for faster lookups
    lookup_df = pd.read_csv(lookup_file)
    lookup_dict = {}

    for _, row in lookup_df.iterrows():
        lookup_dict[row["codebase"]] = (row["main_group"], row["Main_class"])

    # Read the entire file at once
    df = pd.read_csv(input_file)

    # Add new columns with empty strings as default
    df["main_group"] = ""
    df["Main_class"] = ""

    # Process only rows where report is 'mist'
    for idx, row in df.iterrows():
        if row[report_column] == "mist":
            # Extract the code from the name
            name = row[name_column]
            code = extract_code(name)

            # Look up the code in the dictionary and update if found
            if code in lookup_dict:
                main_group, main_class = lookup_dict[code]
                df.at[idx, "main_group"] = main_group
                df.at[idx, "Main_class"] = main_class

    # Write the updated dataframe back to the file
    df.to_csv(input_file, index=False)

    print(f"File {input_file} has been successfully updated with the lookup data.")


if __name__ == "__main__":
    # Default file paths
    input_file = "large_file.csv"
    lookup_file = "lookup_file.csv"

    # Check for command-line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        lookup_file = sys.argv[2]

    # You can specify different column names if needed
    # process_files(input_file, lookup_file, name_column="CustomNameColumn", report_column="CustomReportColumn")

    process_files(input_file, lookup_file)
