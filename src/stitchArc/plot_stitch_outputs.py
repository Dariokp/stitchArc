"""
Reads and processes json files from stitch_outputs.
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

# Plot some metrics from abstraction data
def plot_abstraction_metrics(abstractions_dict):
    """
    Plots abstraction metrics over iterations."
    """
    # Function numbers in sorted order
    fn_numbers = range(len(abstractions_dict))

    # Initialize data lists
    compression_ratios = []
    num_uses = []
    arities = []
    body_lengths = []
    
    # Extract data for each function in order
    for num in fn_numbers:
        fn_key = f'fn_{num}'
        fn_data = abstractions_dict[fn_key]
        
        compression_ratios.append(fn_data['compression_ratio'])
        num_uses.append(fn_data['num_uses'])
        arities.append(fn_data['arity'])
        body_lengths.append(len(fn_data['body']))
    
    all_metrics = [compression_ratios, num_uses, arities, body_lengths]
    all_metrics_names = ['Compression Ratio', 'Number of Uses', 'Arity', 'Function Length']

    # Create a figure with n_rows*n_cols subplots
    n_rows = 2
    n_cols = 2
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(12, 10))
    axs = axs.flatten()
    fig.suptitle('Abstraction Metrics Over Iterations', fontsize=16)
    
    for i in range(n_rows*n_cols):
        axs[i].plot(fn_numbers, all_metrics[i])
        axs[i].set_xlabel('Iteration')
        x_ticks = list(filter(lambda x: x%20==0, fn_numbers))
        axs[i].set_xticks(x_ticks)

        axs[i].set_ylabel(all_metrics_names[i])
        axs[i].grid(True)

    plt.tight_layout()
    # plt.subplots_adjust(top=0.9)
    
    # Save the figure
    plt.savefig('abstraction_metrics.png', dpi=300, bbox_inches='tight')
    
    # Show the plots
    # plt.show()

# Use the function with your data
all_data = load_json_files("stitch_outputs_200")
plot_abstraction_metrics(all_data)