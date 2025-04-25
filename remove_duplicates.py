import pandas as pd
import sys
import os
import tempfile


def remove_duplicates(input_file, output_file=None, columns=None):
    """
    Remove duplicate records from a CSV file.

    Args:
        input_file (str): Path to the input CSV file
        output_file (str, optional): Path to save the output file. If None, overwrites the input file.
        columns (list, optional): List of column names to consider for duplicates. If None, uses all columns.

    Returns:
        int: Number of duplicate records removed
    """
    # Set output file to input file if not specified
    if output_file is None or output_file == "":
        output_file = input_file

    print(f"Processing file: {input_file}")

    try:
        # Read the entire file into memory
        # For very large files, we'd need a different approach
        df = pd.read_csv(input_file)

        # Store original count
        original_count = len(df)
        print(f"Original record count: {original_count}")

        # Use all columns if not specified
        if columns is None:
            columns = df.columns.tolist()
        else:
            # Validate that specified columns exist
            for col in columns:
                if col not in df.columns:
                    raise ValueError(f"Column '{col}' not found in the input file")

        print(f"Checking for duplicates based on columns: {columns}")

        # Identify duplicates
        # keep='first' means we keep the first occurrence and mark all subsequent ones as duplicates
        duplicates = df.duplicated(subset=columns, keep="first")
        duplicate_count = duplicates.sum()

        # Remove duplicates
        df_unique = df.drop_duplicates(subset=columns, keep="first")

        # Calculate statistics
        remaining_count = len(df_unique)
        dup_percentage = (
            (duplicate_count / original_count * 100) if original_count > 0 else 0
        )

        print(f"\nTotal records processed: {original_count}")
        print(f"Unique records: {remaining_count}")
        print(f"Duplicates removed: {duplicate_count} ({dup_percentage:.2f}%)")

        # Write the unique records to the output file
        df_unique.to_csv(output_file, index=False)

        return duplicate_count

    except Exception as e:
        print(f"Error: {e}")
        raise e


if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print(
            "Usage: python remove_duplicates.py input_file.csv [output_file.csv] [column1,column2,...]"
        )
        sys.exit(1)

    input_file = sys.argv[1]

    # Optional output file path
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Optional columns for duplicate checking
    columns = None
    if len(sys.argv) > 3:
        columns = sys.argv[3].split(",")

    # Run the deduplication
    duplicates_removed = remove_duplicates(input_file, output_file, columns)

    print(f"\nSuccessfully removed {duplicates_removed} duplicate records.")
