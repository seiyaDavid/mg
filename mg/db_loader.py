import pandas as pd
import sqlite3
import yaml
import argparse
import os
import logging
import sys
from typing import Dict, List, Any, Optional, Tuple


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Handle configuration loading and validation."""

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
                logger.info(f"Configuration loaded from {config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading configuration: {e}")
            raise


class DataLoader:
    """Handle data loading and preprocessing."""

    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """Load CSV file into a DataFrame."""
        if not os.path.exists(file_path):
            logger.error(f"CSV file not found: {file_path}")
            logger.info("You need to run file_joiner.py first to create the CSV file.")
            raise FileNotFoundError(
                f"File not found: {file_path}. Run file_joiner.py first."
            )

        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} rows from {file_path}")
            return df
        except pd.errors.EmptyDataError:
            logger.error(f"CSV file is empty: {file_path}")
            raise
        except pd.errors.ParserError:
            logger.error(f"Error parsing CSV file: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading CSV file {file_path}: {e}")
            raise


class SchemaInferencer:
    """Infer database schema from DataFrame."""

    @staticmethod
    def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
        """Infer SQL column types from DataFrame dtypes."""
        type_map = {
            "int64": "INTEGER",
            "float64": "REAL",
            "bool": "INTEGER",
            "datetime64[ns]": "TEXT",
            "timedelta64[ns]": "TEXT",
            "object": "TEXT",
        }

        column_types = {}
        for column, dtype in df.dtypes.items():
            sql_type = type_map.get(str(dtype), "TEXT")
            column_types[column] = sql_type

        logger.info(f"Inferred types for {len(column_types)} columns")
        print(column_types)
        return column_types


class DatabaseManager:
    """Handle database operations."""

    def __init__(self, db_path: str):
        """Initialize database manager with database path."""
        self.db_path = db_path
        # Create directory for database if it doesn't exist
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir and not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir)
                logger.info(f"Created directory for database: {db_dir}")
            except OSError as e:
                logger.error(f"Could not create directory for database: {e}")
                raise

        logger.info(f"Database manager initialized with path: {db_path}")

    def create_connection(self) -> sqlite3.Connection:
        """Create a database connection."""
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            logger.error(f"SQLite error connecting to database: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to database: {e}")
            raise

    def create_table(self, table_name: str, column_types: Dict[str, str]) -> None:
        """Create a table with the inferred schema."""
        try:
            columns_def = [
                f'"{column}" {data_type}' for column, data_type in column_types.items()
            ]
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(columns_def)}
            );
            """

            conn = self.create_connection()
            with conn:
                conn.execute(create_table_sql)
            logger.info(f"Table '{table_name}' created or verified")
        except sqlite3.Error as e:
            logger.error(f"SQLite error creating table: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating table: {e}")
            raise

    def insert_data(self, table_name: str, df: pd.DataFrame) -> None:
        """Insert DataFrame data into table."""
        try:
            conn = self.create_connection()
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            logger.info(f"Inserted {len(df)} rows into table '{table_name}'")
        except sqlite3.Error as e:
            logger.error(f"SQLite error inserting data: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error inserting data: {e}")
            raise


class DBLoader:
    """Main class that orchestrates the loading process."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize with optional config path."""
        self.config_path = config_path
        self.config = None
        if config_path:
            try:
                self.config = ConfigManager.load_config(config_path)
            except Exception as e:
                logger.error(
                    f"Failed to initialize DBLoader with config {config_path}: {e}"
                )
                raise

    def load_csv_to_db(self, csv_path: str, db_path: str, table_name: str) -> None:
        """Load CSV data into SQLite database with inferred schema."""
        try:
            # Load data
            df = DataLoader.load_csv(csv_path)

            # Infer schema
            column_types = SchemaInferencer.infer_column_types(df)

            # Create and load database
            db_manager = DatabaseManager(db_path)
            db_manager.create_table(table_name, column_types)
            db_manager.insert_data(table_name, df)

            logger.info(
                f"Successfully loaded {csv_path} into {db_path} as table '{table_name}'"
            )
        except FileNotFoundError as e:
            logger.error(f"File not found error: {e}")
            logger.info("Please run file_joiner.py first to generate the CSV file")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to load CSV to database: {e}")
            sys.exit(1)

    def process_from_config(self) -> None:
        """Process loading based on configuration."""
        if not self.config:
            logger.error("No configuration loaded")
            return

        try:
            csv_path = self.config.get("output_path", "joined_output.csv")
            db_path = self.config.get("database", {}).get("path", "output.db")
            table_name = self.config.get("database", {}).get(
                "table_name", "joined_data"
            )

            # Make the file path absolute if it's not already
            if not os.path.isabs(csv_path):
                csv_path = os.path.abspath(csv_path)

            self.load_csv_to_db(csv_path, db_path, table_name)
        except Exception as e:
            logger.error(f"Error processing from config: {e}")
            sys.exit(1)


def create_integrated_pipeline(config_path: str) -> None:
    """Run the complete data pipeline: join files and load to database."""
    try:
        # First, import and run the file_joiner
        from file_joiner import join_files

        logger.info("Running file_joiner to create the joined CSV file...")

        join_files(config_path)

        # Then, load the CSV to the database
        logger.info("Loading the joined CSV file to the database...")
        loader = DBLoader(config_path)
        loader.process_from_config()

        logger.info("Complete data pipeline executed successfully!")
    except ImportError:
        logger.error(
            "Could not import file_joiner module. Make sure it's in the same directory."
        )
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error in integrated pipeline: {e}")
        sys.exit(1)


def main():
    """Main entry point for the command line interface."""
    parser = argparse.ArgumentParser(
        description="Load CSV file into SQLite database with schema inference"
    )
    parser.add_argument("--config", help="Path to YAML configuration file")
    parser.add_argument("--csv", help="Path to CSV file to load")
    parser.add_argument("--db", default="output.db", help="Path to SQLite database")
    parser.add_argument(
        "--table", default="joined_data", help="Table name to create/replace"
    )
    parser.add_argument(
        "--run-pipeline",
        action="store_true",
        help="Run the complete pipeline (file joining and database loading)",
    )

    args = parser.parse_args()

    try:
        if args.run_pipeline and args.config:
            # Run the full pipeline
            create_integrated_pipeline(args.config)
        elif args.config:
            # Process using configuration file
            loader = DBLoader(args.config)
            loader.process_from_config()
        elif args.csv:
            # Process using command line arguments
            loader = DBLoader()
            loader.load_csv_to_db(args.csv, args.db, args.table)
        else:
            logger.error("Either --config or --csv must be provided")
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
