import os, csv

def write_to_csv(filename, header_row, data_dict):
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if it doesn't exist
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header_row)  # Write header row
        for _, value in data_dict.items():
            writer.writerow(value)  # Write data rows