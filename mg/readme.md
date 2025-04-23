To use this solution:
Install required packages: pip install pandas pyyaml
Update the config.yaml file with your specific file paths and column names
Run the script: python file_joiner.py --config config.yaml
The YAML file allows you to:
Define the paths to each file
Specify the identifier column names in each file
Select which columns you want from file C
Choose different join types (inner, left, right, outer)
Set the output file path.


python db_loader.py --config config.yaml --run-pipeline
