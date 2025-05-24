"""
The purpose of this file is to read stitch functions from stitch_functions and run the Stitch algorithm on all of them.
"""

# General imports
import os
import json
import pprint
import time
import multiprocessing

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # add src to path

from src.stitch_bindings.stitch_core import compress
from stitch_core import compress

def process_json(data):
    """ Remove some unnecessary elements of the json file """
    # data should be a json file

    # For top-level keys "original" and "rewritten", keep only the first element if they are lists
    if "original" in data and isinstance(data["original"], list):
        data["original"] = data["original"][0] if data["original"] else data["original"]

    if "rewritten" in data and isinstance(data["rewritten"], list):
        data["rewritten"] = data["rewritten"][0] if data["rewritten"] else data["rewritten"]

    # Remove the nested key "uses" inside the "abstractions" dictionary if it exists
    if 'abstractions' in data:
        for i in range(len(data['abstractions'])):
            data['abstractions'][i]["uses"] = data['abstractions'][i]["uses"][0]

    return data


if __name__ == "__main__":
    t0 = time.time()
    # Input and output directories
    input_dir = os.path.join(".", "stitch_functions")
    # Create output directory if it doesn't exist
    # os.makedirs(output_dir, exist_ok=True)

    # Determine the number of available CPU threads
    num_threads = multiprocessing.cpu_count()
    # print(f"Number of available CPU threads: {num_threads}")

    # print("Current file path: ", __file__)
    # print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    # print(f"Current dir: {os.getcwd()}")

    # Read all files in the input directory and save them in a list
    stitch_functions = []
    for file_path in os.listdir(input_dir):
        with open(os.path.join(input_dir, file_path), 'r') as f:
            stitch_functions.append(f.read())

    # Create directory for outputs
    stitch_output_dir = "stitch_outputs"
    os.makedirs(stitch_output_dir, exist_ok=True)

    # Determines how many abstractions Stitch will construct
    n_iterations = 5
    latest_programs = stitch_functions
    print("Compressing...")
    for i in range(n_iterations):
        # Run the Stitch algorithm on all functions
        res = compress(latest_programs, iterations=1, max_arity=2, threads=num_threads-1, previous_abstractions=i)

        # Save intermediate result
        updated_data = process_json(res.json)
        file_path = os.path.join(stitch_output_dir, f'stitch_output_{i+1}.json')
        with open(file_path, 'w') as f:
            json.dump(updated_data, f, indent=4)

        # Update the programs with the rewritten version
        latest_programs = res.rewritten

        # Print progress every 10th iterations
        if (i+1) % 10 == 0:
            print(f"Iteration {i+1} completed | {time.time() - t0:.2f} seconds elapsed | current abstraction: {res.abstractions}")


    # print(res.abstractions)
    # print(res.rewritten)
    # pprint.pp(res.json)

    print(f"Finished compressing in {time.time() - t0:.2f} seconds")
