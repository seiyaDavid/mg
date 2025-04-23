import pandas as pd
import yaml
import argparse


def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def join_files(config_path, return_identifier="a"):
    """Join files based on configuration.

    Args:
        config_path: Path to the configuration YAML file
        return_identifier: Which identifier to return ('a', 'b', or 'c')

    Returns:
        DataFrame containing just the specified identifier column
    """
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
    )

    # Join with C
    final_df = pd.merge(
        merged_ab,
        df_c,
        left_on=file_a_id,  # Using A's ID as the join key
        right_on=file_c_id,
        how=config.get("join_type_c", "left"),
    )

    # Save to output file
    output_path = config.get("output_path", "joined_output.csv")
    final_df.to_csv(output_path, index=False)
    print(f"Joined data saved to {output_path}")

    # Return just the identifier column based on user's choice
    if return_identifier == "a":
        return final_df[[file_a_id]]
    elif return_identifier == "b":
        return final_df[[file_b_id]]
    elif return_identifier == "c":
        return final_df[[file_c_id]]
    else:
        raise ValueError("return_identifier must be 'a', 'b', or 'c'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Join multiple files based on identifiers"
    )
    parser.add_argument(
        "--config", required=True, help="Path to YAML configuration file"
    )
    args = parser.parse_args()

    # Returns DataFrame with just file_a_id column
    id_df = join_files(args.config, return_identifier="a")

    # Or for file_b_id
    id_df = join_files(args.config, return_identifier="b")
