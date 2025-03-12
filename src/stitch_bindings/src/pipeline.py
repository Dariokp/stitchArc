
# Expects to be called from ./src/stitch_bindings/src

import os
import sys

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

print(os.getcwd())

from flatliner.flatliner import Flatliner
from flatliner.transformations import transform_lambda

from LOTlib3.StitchBindings.python_to_stitch import python_to_stitch

# Path to file that should be flattened
file_to_flatten_path = os.path.join("re-arc_generator.py")

# Flatten
test = Flatliner()
test.set_ast(file_to_flatten_path)
lambda_exp = test.unparse()

# Format flattened lambda
lambda_exp_cleaned = transform_lambda(lambda_exp)

# Translate to Stitch
stitch_exp = python_to_stitch(lambda_exp)

print(stitch_exp)