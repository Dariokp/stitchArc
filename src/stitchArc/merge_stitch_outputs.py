"""
Merge the json output files into a single large json file.
"""

# General imports
import os
import json

def load_and_merge_json_files(input_dir, save=True):
    """
    Load and merge json files according to specific requirements.
    """
    # Get list of files
    file_paths = os.listdir(input_dir)
    
    # Sort files based on numeric part in the filename
    def extract_number(filename):
        return int(filename.split('_')[-1].split('.')[0])
    
    file_paths = sorted(file_paths, key=extract_number)
            
    # Load first file as template
    with open(os.path.join(input_dir, file_paths[0]), 'r') as f:
        merged_data = json.load(f)
    
    # Process subsequent files
    for i, file_path in enumerate(file_paths[1:], 1):
        # print(f"Processing file {i+1}: {file_path}")
        with open(os.path.join(input_dir, file_path), 'r') as f:
            current_data = json.load(f)
        
        # Increment iterations, previous_abstractions, and num_abstractions
        merged_data["args"]["iterations"] += 1
        merged_data["num_abstractions"] += 1

        # Update compression_ratio
        if current_data["abstractions"]:
            # Update compression ratio using the new abstraction
            new_abstraction = current_data["abstractions"][0]
            merged_data["compression_ratio"] *= new_abstraction["compression_ratio"]
    
            # Get new abstraction
            new_abstraction = current_data["abstractions"][0]
            
            # Update cumulative_compression_ratio in the new abstraction
            prev_cumulative = merged_data["abstractions"][-1]["cumulative_compression_ratio"]
            new_abstraction["cumulative_compression_ratio"] *= prev_cumulative
            
            # Add new abstraction to the list
            merged_data["abstractions"].append(new_abstraction)
    
    # Update final_cost using the last file
    merged_data["final_cost"] = current_data["final_cost"]

    print(f"Successfully merged {len(file_paths)} files")

    if save:
        output_file = os.path.join(input_dir, "merged_output.json")
        with open(output_file, 'w') as f:
            json.dump(merged_data, f, indent=4)
        print(f"Saved merged data to {output_file}")

    return merged_data

load_and_merge_json_files("stitch_outputs_200")