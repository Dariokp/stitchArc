"""
The purpose of this file is to acquire abstracted Stitch functions from re-arc python functions.

This mainly involves combining re-arc, flatliner, LOTlib3, and stitch_bindings to transform re-arc (python) functions into functions that Stitch can be used on.
"""
# General imports
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # add src to path
from tqdm import tqdm

# Flatliner and transformation imports
from src.flatliner.flatliner import Flatliner
from src.flatliner.transformations import transform_lambda

# LOTlib3 imports
from src.LOTlib3.StitchBindings.python_to_stitch import python_to_stitch

# Read generator files from src/reArc/generator_functions, flatten and transform them into the suitable format for LOTlib3, then transform them into Stitch functions and save them in src/stitchArc/stitch_functions


def process_and_save_file(input_file, output_dir, filename):
    """
    Process a file with transform_lambda and save the result
    
    Args:
        input_file: Path to the input file
        output_dir: Directory to save the output
        filename: Custom filename (does not use default)
    """
    
    # Process the file using flatliner and the transformations
    test = Flatliner()
    test.set_ast(input_file)
    lambda_f = test.unparse()
    lambda_transformed_f = transform_lambda(lambda_f)

    try:
        # Use LOTlib3 to transform the result into a Stitch function
        stitch_f = python_to_stitch(lambda_transformed_f)
    except Exception as e:
        print(f"\tError transforming to Stitch | {filename} : {e}")        

    # Save the result
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w') as f:
        f.write(stitch_f)
    

# def load_processed_files(directory, pattern="*.lambda"):
#     """
#     Load all processed files from a directory into a list of strings
    
#     Args:
#         directory: Directory containing the processed files
#         pattern: File pattern to match (default: *.lambda)
    
#     Returns:
#         List of strings, each containing the contents of a file
#     """
#     results = []
#     for file_path in sorted(glob.glob(os.path.join(directory, pattern))):
#         with open(file_path, 'r') as f:
#             results.append(f.read())
#     return results

if __name__ == "__main__":
    # Input and output directories
    input_dir = os.path.join("..", "reArc", "generator_functions")
    output_dir = os.path.join(".", "stitch_functions")
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # unsucessful files:
    unsuccessful_files = [
        "generate_b782dc8a.py",
        "generate_ae3edfdc.py",
        "generate_85c4e7cd.py",
        "generate_a78176bb.py", 
        "generate_36d67576.py",
        "generate_234bbc79.py",
        "generate_bda2d7a6.py",
        "generate_1f642eb9.py",
        "generate_08ed6ac7.py",
        "generate_9af7a82c.py",
        "generate_29c11459.py",
        "generate_beb8660c.py",
        "generate_22eb0ac0.py",
        "generate_e73095fd.py",
    ]
    
    # Process all files in the input directory
    for file_path in tqdm(os.listdir(input_dir), desc="Transforming generator files to lambda expressions"):
        file_name = file_path.split("_")[1].strip(".py")
        
        # Skip unsuccessful files
        if file_name in map(lambda x: x.strip(".py"), unsuccessful_files):
            continue
        
        try:
            process_and_save_file(os.path.join(input_dir, file_path), output_dir, file_name)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
