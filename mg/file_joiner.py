import pandas as pd
import yaml
import argparse


def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def join_files(config_path):
    """Join files based on configuration."""
    # Load configuration
    config = load_config(config_path)

    # Extract configuration details
    file_a_path = config["files"]["a"]["path"]
    file_b_path = config["files"]["b"]["path"]
    file_c_path = config["files"]["c"]["path"]

    file_a_id = config["files"]["a"]["id_column"]
    file_b_id = config["files"]["b"]["id_column"]
    file_c_id = config["files"]["c"]["id_column"]

    # Columns to select from file C
    c_columns = [file_c_id] + config.get("columns_from_c", [])

    # Read data
    df_a = pd.read_csv(file_a_path)
    df_b = pd.read_csv(file_b_path)
    df_c = pd.read_csv(file_c_path)

    # Select only needed columns from C
    df_c = df_c[c_columns]

    # Join A and B
    merged_ab = pd.merge(
        df_a,
        df_b,
        left_on=file_a_id,
        right_on=file_b_id,
        how=config.get("join_type", "inner"),
        suffixes=(
            "",
            "_b",
        ),  # Keep A's columns without suffix, add _b to B's duplicates
    )

    # Join with C
    final_df = pd.merge(
        merged_ab,
        df_c,
        left_on=file_a_id,  # Using A's ID as the join key
        right_on=file_c_id,
        how=config.get("join_type_c", "left"),
        suffixes=(
            "",
            "_c",
        ),  # Keep existing columns without suffix, add _c to C's duplicates
    )

    # Check if we should keep only the identifier from dataset A
    if config.get("keep_only_a_identifier", False):
        # Drop the identifier columns from datasets B and C
        cols_to_drop = [file_b_id, file_c_id]
        final_df = final_df.drop(columns=cols_to_drop)
        print("Keeping only the identifier from dataset A")

    # Handle redundant fields
    redundant_fields = config.get("redundant_fields", [])
    for field_config in redundant_fields:
        column = field_config.get("column")
        keep_from = field_config.get("keep_from")

        if column and keep_from:
            # Find all column names that match the pattern (including suffixed versions)
            duplicate_cols = [
                col for col in final_df.columns if column in col and col != column
            ]

            # Drop the duplicate columns
            if duplicate_cols:
                final_df = final_df.drop(columns=duplicate_cols)
                print(f"Removed redundant columns for '{column}': {duplicate_cols}")

    # Save to output file
    output_path = config.get("output_path", "joined_output.csv")
    final_df.to_csv(output_path, index=False)
    print(f"Joined data saved to {output_path}")

    return final_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Join multiple files based on identifiers"
    )
    parser.add_argument(
        "--config", required=True, help="Path to YAML configuration file"
    )
    args = parser.parse_args()

    join_files(args.config)
