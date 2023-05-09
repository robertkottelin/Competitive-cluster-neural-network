import pandas as pd
import numpy as np
import re

def process_file(input_file, output_file):
    # Load the data
    df = pd.read_csv(input_file, quotechar='"')

    # Extract FAM_vector data
    fam_vectors = df["FAM_vector"]

    # Process vectors into a format that Rust can read
    formatted_vectors = []
    for vector in fam_vectors:
        # Use regex to find all numbers in the string
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", vector)

        # Convert to floats and format as Rust array
        float_numbers = [float(num) for num in numbers]
        formatted_vector = f"{float_numbers},"

        formatted_vectors.append(formatted_vector)

    # Write to output file
    with open(output_file, "w") as f:
        for vector in formatted_vectors:
            f.write(vector + "\n")

if __name__ == "__main__":
    process_file("vectors.txt", "formatted_vectors.txt")
