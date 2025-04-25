import pandas as pd

# Sample main dataframe
df_main = pd.DataFrame({
    'Name': ['COMP PETER', 'EVT MAKES', 'DVD PLAY'],
    'Category': ['UTILITY', 'Cooking', 'Watch'],
    'age': [34, 34, 23],
    'main_group': ['dataScience', 'analytics', 'besic'],
    'Main_class': ['analytics', 'basicPackage', 'package'],
    'codebase': ['', '', '']  # some empty cells
})

# Lookup dataframe
df_lookup = pd.DataFrame({
    'codebase': ['COMP', 'EVT', 'DVD'],
    'main_group': ['dataScience', 'analytics', 'Play'],
    'Main_class': ['analytics', 'basicPackage', 'models']
})

# Extract potential code from 'Name'
df_main['_name_code'] = df_main['Name'].fillna('').str.extract(r'^(\w+)')

# Merge only for rows with Category == 'UTILITY'
df_main_utility = df_main[df_main['Category'] == 'UTILITY'].copy()

df_merged = df_main_utility.merge(
    df_lookup,
    left_on='_name_code',
    right_on='codebase',
    how='left',
    suffixes=('', '_lookup')
)

# Apply updates conditionally
for col in ['main_group', 'Main_class']:
    df_main.loc[df_merged.index, col] = df_merged[f'{col}_lookup'].combine_first(df_merged[col])

# Update empty codebase in main only where lookup match was found
df_main.loc[df_merged.index, 'codebase'] = df_main.loc[df_merged.index, 'codebase'].replace('', pd.NA)
df_main.loc[df_merged.index, 'codebase'] = df_main.loc[df_merged.index, 'codebase'].combine_first(df_merged['codebase'])

# Drop temporary column
df_main.drop(columns=['_name_code'], inplace=True)

print(df_main)
