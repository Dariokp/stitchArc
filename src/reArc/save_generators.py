import os
import re

def extract_generator_functions(input_file, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the input file
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Split the content into lines
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a generator function
        match = re.match(r'^def (generate_[a-z0-9]+)\(diff_lb: float, diff_ub: float\) -> dict:', line)
        if match:
            func_name = match.group(1)
            
            # Get the indentation level (should be 0 for function definition)
            indent_level = len(line) - len(line.lstrip())
            
            # Collect all lines of this function
            func_lines = [line]
            j = i + 1
            
            # Continue until we reach another function definition or end of file
            while j < len(lines) and (
                lines[j].strip() == "" or 
                len(lines[j]) - len(lines[j].lstrip()) > indent_level or
                not lines[j].strip().startswith("def ")
            ):
                func_lines.append(lines[j])
                j += 1
            
            # Combine the lines to form the complete function
            complete_func = '\n'.join(func_lines)
            
            # Skip incomplete functions
            if "..." in complete_func:
                print(f"Skipping incomplete function: {func_name}")
            else:
                # Create output file path
                output_file = os.path.join(output_dir, f"{func_name}.py")
                
                # Add the necessary imports
                # imports = "from dsl import *\nfrom utils import *\n\n"
                
                # Write the function to the file
                with open(output_file, 'w') as f:
                    f.write(complete_func)
                
                # print(f"Saved: {output_file}")
            
            # Move to the next line after this function
            i = j
        else:
            # Move to the next line
            i += 1

if __name__ == "__main__":
    input_file = "generators.py"
    output_dir = "generator_functions"

    extract_generator_functions(input_file, output_dir)
    print(f"Done! Functions saved to {output_dir}/")

    # Check size of output_dir (should be 400)
    out_dir_len = len(os.listdir(output_dir))
    expected_length = 400
    if out_dir_len == expected_length:
        print(f"Output directory has the expected number of functions ({expected_length}).")
    else:
        print(f"Output directory does not have the expected number of functions. Found: {out_dir_len}, Expected: {expected_length}")
