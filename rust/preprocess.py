import pandas as pd
import re

def process_file(input_file, output_file):
    # Load the data
    df = pd.read_csv(input_file, quotechar='"')

    # Process each vector column into a format that Rust can read
    formatted_vectors = []
    for col in df.columns:
        # Ignore non-vector columns
        if col.endswith("_vector"):
            # Extract vector data
            vectors = df[col]
            # Process vectors into a format that Rust can read
            for vector in vectors:
                # Use regex to find all numbers in the string
                numbers = re.findall(r"[-+]?\d*\.\d+e[-+]?\d+", vector)

                # Convert to floats and format as Rust array
                float_numbers = [float(num) for num in numbers]
                formatted_vector = " ".join(f"{num}" for num in float_numbers)

                formatted_vectors.append(formatted_vector)

    # Remove empty lines
    formatted_vectors = [vector for vector in formatted_vectors if vector]

    # Write to output file
    with open(output_file, "w") as f:
        f.write("\n".join(formatted_vectors))

if __name__ == "__main__":
    process_file("vectors.txt", "formatted_vectors_all.txt")
