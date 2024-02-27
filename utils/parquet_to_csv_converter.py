import os
import sys
import pyarrow.parquet as pq


def convert_parquet_to_csv(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".parquet"):
                parquet_file = os.path.join(root, file)
                csv_file = os.path.splitext(parquet_file)[0] + ".csv"
                table = pq.read_table(parquet_file)
                table.to_pandas().to_csv(csv_file, index=False)
                print(f"Converted {parquet_file} to {csv_file}")


def remove_parquet_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".parquet"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Removed {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py folder_path")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    convert_parquet_to_csv(folder_path)
    # remove_parquet_files(folder_path)
