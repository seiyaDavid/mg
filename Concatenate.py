import pandas as pd

def merge_files_with_selected_columns(file_a_path, file_b_path, output_path='merged_output.csv', 
                                      allowed_extra_columns=None):
    """
    Merge two CSV files based on common columns and optionally include only selected extra columns from file B.

    Parameters:
        file_a_path (str): Path to the first CSV file.
        file_b_path (str): Path to the second CSV file.
        output_path (str): Path to save the merged file.
        allowed_extra_columns (list of str): Extra columns from file B to keep (e.g., ['code']).
    """
    df_a = pd.read_csv(file_a_path)
    df_b = pd.read_csv(file_b_path)

    # Common columns
    common_cols = list(set(df_a.columns) & set(df_b.columns))

    # Keep only selected extra columns from B
    if allowed_extra_columns:
        # Keep only if they actually exist in df_b
        allowed_extra_columns = [col for col in allowed_extra_columns if col in df_b.columns]
    else:
        allowed_extra_columns = []

    # Final column order: common columns (from df_a's order) + allowed extra columns
    ordered_common = [col for col in df_a.columns if col in common_cols]
    final_columns = ordered_common + allowed_extra_columns

    # Add missing allowed columns to df_a
    for col in allowed_extra_columns:
        df_a[col] = pd.NA

    # Subset both dataframes
    df_a = df_a[final_columns]
    df_b = df_b[final_columns]

    # Concatenate and save
    merged_df = pd.concat([df_a, df_b], ignore_index=True)
    merged_df.to_csv(output_path, index=False)
    print(f"Merged file saved as: {output_path}")
