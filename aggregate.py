import pandas as pd

def compute_hit_percentages(filepath: str) -> pd.DataFrame:
    """
    Computes the percentage of hits for each Sub_Category ('Gold', 'Silver', 'Bronse')
    per empName and Category combination.

    Parameters:
        filepath (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: A pivoted DataFrame with percentages of Sub_Categories.
    """
    # Load CSV
    # df = pd.read_csv(filepath)

    # Group by empName, Category, Sub_Category to sum hits
    grouped = df.groupby(['empName', 'Category', 'Sub_Category'], as_index=False)['Hit'].sum()

    # Total hits per empName and Category
    total_hits = grouped.groupby(['empName', 'Category'])['Hit'].sum().reset_index(name='TotalHit')

    # Merge total back
    merged = pd.merge(grouped, total_hits, on=['empName', 'Category'])

    # Calculate percentage
    merged['Percentage'] = (merged['Hit'] / merged['TotalHit'] * 100).round(0).astype(int).astype(str) + '%'

    # Pivot to get Sub_Category as columns
    pivot = merged.pivot(index=['empName', 'Category'], columns='Sub_Category', values='Percentage').reset_index()

    # Ensure all expected Sub_Category columns are present
    for col in ['Gold', 'Silver', 'Bronse']:
        if col not in pivot.columns:
            pivot[col] = '0%'

    # Fill NaNs with '0%'
    pivot = pivot.fillna('0%')

    # Reorder columns
    pivot = pivot[['empName', 'Category', 'Gold', 'Silver', 'Bronse']]

    return pivot


result_df = compute_hit_percentages(df)

# Print to console
print(result_df.to_string(index=False))

# Write to CSV
# result_df.to_csv('output_percentages.csv', index=False)
