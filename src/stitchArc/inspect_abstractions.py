"""
Reads output files and extracts the abstractions.
"""

# General imports
import os
import json
import matplotlib.pyplot as plt
import re
import numpy as np

# Extract the abstraction and its compression score from a json output file
def get_json_info(json_dict):
    
    abst_dict = json_dict.get("abstractions")[0]
    abst_name = abst_dict.get("name")
    abst_body = abst_dict.get("body")
    abst_arity = abst_dict.get("arity")
    abst_nuses = abst_dict.get("num_uses")
    
    return { abst_name : 
                {"body": abst_body,
                "arity": abst_arity,
                "num_uses": abst_nuses,
                "compression_ratio": json_dict.get("compression_ratio") }
        }

# Load the json files from stitch_outputs
def load_json_files(input_dir):
    """
    Load all json files in the input directory.
    """
    all_data = {}
    
    for file_path in sorted(os.listdir(input_dir)):
        with open(os.path.join(input_dir, file_path), 'r') as f:
            data = json.load(f)            
            data = get_json_info(data)
            all_data.update(data)
    
    return all_data

def write_abstractions_to_txt(abstractions_dict, output_file="abstraction_summary.txt"):
    """
    Creates a formatted text file with proper alignment, displaying full content.
    """
    # Sort keys to ensure correct ordering
    keys = sorted(abstractions_dict.keys(), 
                 key=lambda k: int(k.split('_')[1]) if k.startswith('fn_') else 0)
    
    # Calculate column widths for alignment
    max_key_len = max(len(key) for key in keys)
    max_arity_len = max(len(str(data['arity'])) for data in abstractions_dict.values())
    max_ratio_len = 12  # Fixed width for compression ratio
    max_uses_len = max(len(str(data['num_uses'])) for data in abstractions_dict.values())
    
    # Create the output file with better formatting
    with open(output_file, 'w') as f:
        # Write header
        header = f"{'FUNCTION':<{max_key_len}}\t| {'ARITY':<{max_arity_len}}\t| {'COMPRESSION':<{max_ratio_len}}\t| {'USES':<{max_uses_len}}\t| BODY"
        f.write(header + "\n")
        f.write("=" * len(header) + "\n")
        
        # Write each abstraction
        for key in keys:
            data = abstractions_dict[key]
            
            # First line with function name, arity, compression ratio, uses
            f.write(f"{key:<{max_key_len}}\t\t| {data['arity']:<{max_arity_len}}\t\t| {data['compression_ratio']:<{max_ratio_len}.2f}\t| {data['num_uses']:<{max_uses_len}}\t| ")
            
            # Add the body (no truncation)
            body_lines = data['body'].split('\n')
            
            # First line of body continues on the same line
            f.write(f"{body_lines[0]}\n")
            
            # Any additional lines are properly indented
            indent = " " * (max_key_len + 3 + max_arity_len + 3 + max_ratio_len + 3 + max_uses_len + 3)
            for line in body_lines[1:]:
                f.write(f"{indent}{line}\n")
            
            # Add a separator line between abstractions
            f.write("-" * len(header) + "\n")
    
    print(f"Enhanced abstraction summary written to {output_file}")

# Load the json files
input_dir = "stitch_outputs_200"
abstractions_dict = load_json_files(input_dir)
write_abstractions_to_txt(abstractions_dict)