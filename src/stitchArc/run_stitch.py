"""
The purpose of this file is to read stitch functions from stitch_functions and run the Stitch algorithm on all of them.
"""

# General imports
import os
import json
import pprint
import time

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # add src to path

from src.stitch_bindings.stitch_core import compress


if __name__ == "__main__":
    t0 = time.time()
    # Input and output directories
    input_dir = os.path.join(".", "stitch_functions")
    # Create output directory if it doesn't exist
    # os.makedirs(output_dir, exist_ok=True)

    # Read all files in the input directory and save them in a list
    stitch_functions = []
    for file_path in os.listdir(input_dir):
        with open(os.path.join(input_dir, file_path), 'r') as f:
            stitch_functions.append(f.read())
    
    # Run the Stitch algorithm on all functions
    res = compress(stitch_functions[:10], iterations=1, max_arity=3, threads=6)

    # print(res.abstractions)
    # print(res.rewritten)
    
    # Save the json file
    with open(os.path.join(".", "stitch_output.json"), 'w') as f:
        json.dump(res.json, f, indent=4)

    # pprint.pp(res.json)

    print(f"Finished compressing in {time.time() - t0:.2f} seconds")
