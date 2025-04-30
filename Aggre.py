import pandas as pd

def compute_hit_percentages(filepath: str) -> pd.DataFrame:
    """
    Computes the percentage of hits for each Sub_Category per empName
    (ignoring Category in grouping) and returns a DataFrame.

    Parameters:
        filepath (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: empName, Category, and Sub_Category percentages.
    """
    df = pd.read_csv(filepath)

    # Sum Hit for each empName and Sub_Category
    sub_totals = df.groupby(['empName', 'Sub_Category'], as_index=False)['Hit'].sum()

    # Total Hit per empName
    total_hits = sub_totals.groupby('empName')['Hit'].sum().reset_index(name='TotalHit')

    # Merge totals to compute percentage
    merged = pd.merge(sub_totals, total_hits, on='empName')
    merged['Percentage'] = (merged['Hit'] / merged['TotalHit'] * 100).round(0).astype(int).astype(str) + '%'

    # Get one Category per empName (if needed, use first occurrence)
    categories = df.groupby('empName')['Category'].first().reset_index()

    # Pivot to Sub_Category as columns
    pivot = merged.pivot(index='empName', columns='Sub_Category', values='Percentage').reset_index()

    # Merge Category back
    pivot = pd.merge(pivot, categories, on='empName')

    # Fill missing sub-categories with '0%'
    for col in ['Gold', 'Silver', 'Bronse']:
        if col not in pivot.columns:
            pivot[col] = '0%'
    pivot = pivot.fillna('0%')

    # Rearrange columns
    final_df = pivot[['empName', 'Category', 'Gold', 'Silver', 'Bronse']]

    return final_df
