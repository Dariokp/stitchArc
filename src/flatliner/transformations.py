"""
    This file transforms one-lined lambda expressions into a form compatible with the Python-to-Stitch translator. 
    It applies a series of AST transformations to curry and clean the expressions.

    Example transformation

        Input:  lambda x, y: x + y if x > 0 else x * y
        
        Output: lambda x1: lambda x2: ifElse(gt(x1)(0))(add(x1)(x2))(mul(x1)(x2))
"""

import ast
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # add src to path

from src.flatliner.flatliner import Flatliner

class CurryTransformer(ast.NodeTransformer):
    def visit_Lambda(self, node):
        # First, process child nodes.
        node = self.generic_visit(node)

        # Handle *args if present
        if node.args.vararg:
            # Get the variable arg name and keep it as is
            vararg_name = node.args.vararg.arg
            
            # Create a regular parameter with the original name
            new_arg = ast.arg(arg=vararg_name, annotation=None)
            node.args.args.append(new_arg)
            node.args.vararg = None
            
        # If the lambda has one (or zero) argument, nothing to do.
        if len(node.args.args) <= 1:
            return node
        # For multiple arguments, transform:
        # lambda x, y, ...: body  -->  lambda x: lambda y: ... (nested lambdas)
        args_list = node.args.args
        new_body = node.body
        # Nest lambdas from the last argument to the first.
        for arg in reversed(args_list):
            new_body = ast.Lambda(
                args=ast.arguments(
                    posonlyargs=[],
                    args=[arg],
                    vararg=None,
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]
                ),
                body=new_body
            )
        return new_body

    def visit_Call(self, node):
        # Process function and argument expressions first.
        node = self.generic_visit(node)
        # If there's one or zero arguments, nothing to do.
        if len(node.args) <= 1:
            return node
        # For calls with multiple arguments, curry them:
        # f(a, b, c)  -->  f(a)(b)(c)
        new_node = node.func
        for arg in node.args:
            new_node = ast.Call(func=new_node, args=[arg], keywords=[])
        return new_node

class OperatorTransformer(ast.NodeTransformer):
    OP_MAP = {
        # Binary operators
        ast.Add: "add",
        ast.Sub: "sub",
        ast.Mult: "mul",
        ast.FloorDiv: "floordiv",
        # Comparison operators
        ast.Eq: "eq",
        ast.NotEq: "neq",
        ast.Lt: "lt",    
        ast.LtE: "lte",  
        ast.Gt: "gt",    
        ast.GtE: "gte",
        ast.In: "elem",
        ast.NotIn: "nelem",
        ast.Is: "isComp",
        ast.IsNot: "isNot",
    }

    def visit_BinOp(self, node):
        # Convert binary operators (+, -, *, //, etc.)
        func_name = self.OP_MAP.get(type(node.op))
        if func_name:
            return ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=[self.visit(node.left), self.visit(node.right)],
                keywords=[]
            )
        return self.generic_visit(node)

    def visit_Compare(self, node):
        # First, process children nodes
        # node = self.generic_visit(node)
        
        # If there's only one comparison, handle it as before.
        if len(node.ops) == 1:
            op_type = type(node.ops[0])
            func_name = self.OP_MAP.get(op_type)
            if func_name:
                return ast.Call(
                    func=ast.Name(id=func_name, ctx=ast.Load()),
                    args=[node.left, node.comparators[0]],
                    keywords=[]
                )
        
        # For chain comparisons like x == y == 1, build a BoolOp (x == y) and (y == 1)
        comparisons = []
        left = node.left
        for op, comparator in zip(node.ops, node.comparators):
            func_name = self.OP_MAP.get(type(op))
            if func_name is None:
                # If we don't have a mapping for an operator, fallback.
                return self.generic_visit(node)
            comp_call = ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=[left, comparator],
                keywords=[]
            )
            comparisons.append(comp_call)
            left = comparator  # Next left-hand side is the previous comparator
        
        # Combine all comparisons with a logical and.
        return ast.BoolOp(
            op=ast.And(),
            values=comparisons
        )

class BoolOpTransformer(ast.NodeTransformer):
    OP_MAP = {
        ast.And: "andOp",
        ast.Or:  "orOp"
    }
    
    def visit_BoolOp(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Get the function name for this Boolean operator
        func_name = self.OP_MAP.get(type(node.op))
        if not func_name:
            return node
            
        # For expressions with more than 2 values, we need to chain them:
        # a and b and c becomes __and__(a, __and__(b, c))
        if len(node.values) > 2:
            # Start with the rightmost pair of values
            result = ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=[node.values[-2], node.values[-1]],
                keywords=[]
            )
            
            # Chain the remaining values from right to left
            for value in reversed(node.values[:-2]):
                result = ast.Call(
                    func=ast.Name(id=func_name, ctx=ast.Load()),
                    args=[value, result],
                    keywords=[]
                )
            return result
        else:
            # Simple case: just two values
            return ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=[node.values[0], node.values[1]],
                keywords=[]
            )

class BitOpTransformer(ast.NodeTransformer):
    """
    Transforms bitwise operations (|, &, ^, ~, <<, >>) into function calls.
    For example:
      a | b  -->  bitOr(a, b)
      x & y  -->  bitAnd(x, y)
    """
    OP_MAP = {
        ast.BitOr: "bitOr",
        ast.BitAnd: "bitAnd",
        ast.BitXor: "bitXor",
        ast.LShift: "lshift",
        ast.RShift: "rshift"
    }
    
    def visit_BinOp(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Get the function name for this bitwise operator
        func_name = self.OP_MAP.get(type(node.op))
        if not func_name:
            return node
            
        # Convert the bitwise operation to a function call
        return ast.Call(
            func=ast.Name(id=func_name, ctx=ast.Load()),
            args=[node.left, node.right],
            keywords=[]
        )
        
    def visit_UnaryOp(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Handle bitwise not (~)
        if isinstance(node.op, ast.Invert):
            return ast.Call(
                func=ast.Name(id="__bitNot__", ctx=ast.Load()),
                args=[node.operand],
                keywords=[]
            )
        return node

class IfExpTransformer(ast.NodeTransformer):
    """Transforms if-else expressions into function calls"""
    
    def visit_IfExp(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Convert the if-expression into a function call:
        # x if y else z  -->  ifElse(y)(x)(z)
        return ast.Call(
            func=ast.Name(id="ifElse", ctx=ast.Load()),
            args=[node.test, node.body, node.orelse],
            keywords=[]
        )

class TaggerTransformer(ast.NodeTransformer):
    """ Tags occurences like [132,3,10] as __list__(132, 3, 10).
     
            Supported tags are:
            - Lists,
            - list comprehension,
            - list indexing,
            - tuples,
            - strings,
            - sets,
            - dictionaries,
            - kleene stars (*).
    """

    def visit_List(self, node):
        # Wrap the tuple elements in a call to a special function.
        new_node = ast.Call(
            func=ast.Name(id="__list__", ctx=ast.Load()),
            args=node.elts,
            keywords=[]
        )
        return ast.copy_location(new_node, node)
    
    def visit_ListComp(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Extract components of the list comprehension
        expr = node.elt
        generators = node.generators
        
        # For each generator, extract its parts
        transformed_generators = []
        for gen in generators:
            target = gen.target
            iter_expr = gen.iter
            ifs = gen.ifs
            
            # Create a representation for this generator
            gen_dict = {
                'target': target,
                'iter': iter_expr,
                'ifs': ifs
            }
            transformed_generators.append(gen_dict)
        
        # Create calls for each component in a curried style
        result = ast.Call(
            func=ast.Name(id='__listComp__', ctx=ast.Load()),
            args=[expr],  # Expression to evaluate for each item
            keywords=[]
        )
        
        # Add each generator's components
        for gen in transformed_generators:
            # Add the target variable
            result = ast.Call(
                func=result,
                args=[gen['target']],
                keywords=[]
            )
            
            # Add the iterable
            result = ast.Call(
                func=result,
                args=[gen['iter']],
                keywords=[]
            )
            
            # Add conditions as a list of lambdas
            if gen['ifs']:
                for if_expr in gen['ifs']:
                    # Create a lambda for each condition
                    result = ast.Call(
                        func=result,
                        args=[if_expr],
                        keywords=[]
                    )
        
        return ast.copy_location(result, node)
    
    def visit_Subscript(self, node):
        # First process any nested nodes within value and slice
        node = self.generic_visit(node)
        
        # Handle different slice types
        if isinstance(node.slice, ast.Slice):
            slice_node = node.slice
            
            # Case 1: x[:upper] -> getItemUpTo(x)(upper)
            if slice_node.lower is None and slice_node.upper is not None and slice_node.step is None:
                return ast.Call(
                    func=ast.Call(
                        func=ast.Name(id="getItemUpTo", ctx=ast.Load()),
                        args=[node.value],
                        keywords=[]
                    ),
                    args=[slice_node.upper],
                    keywords=[]
                )
            
            # Case 2: x[lower:upper] -> getItemFromTo(x)(lower)(upper)
            elif slice_node.lower is not None and slice_node.upper is not None and slice_node.step is None:
                return ast.Call(
                    func=ast.Call(
                        func=ast.Call(
                            func=ast.Name(id="getItemFromTo", ctx=ast.Load()),
                            args=[node.value],
                            keywords=[]
                        ),
                        args=[slice_node.lower],
                        keywords=[]
                    ),
                    args=[slice_node.upper],
                    keywords=[]
                )
            
            # Case 3: x[lower:] -> getItemFrom(x)(lower)
            elif slice_node.lower is not None and slice_node.upper is None and slice_node.step is None:
                return ast.Call(
                    func=ast.Call(
                        func=ast.Name(id="getItemFrom", ctx=ast.Load()),
                        args=[node.value],
                        keywords=[]
                    ),
                    args=[slice_node.lower],
                    keywords=[]
                )
            
            # Case 4: x[::step] -> getItemWithStep(x)(0)(-1)(step)
            elif slice_node.step is not None:
                # Default lower bound is 0 if not specified
                lower = slice_node.lower if slice_node.lower is not None else ast.Constant(value=0)
                # Default upper bound is -1 (representing end) if not specified
                upper = slice_node.upper if slice_node.upper is not None else ast.Constant(value=-1)
                
                return ast.Call(
                    func=ast.Call(
                        func=ast.Call(
                            func=ast.Call(
                                func=ast.Name(id="getItemWithStep", ctx=ast.Load()),
                                args=[node.value],
                                keywords=[]
                            ),
                            args=[lower],
                            keywords=[]
                        ),
                        args=[upper],
                        keywords=[]
                    ),
                    args=[slice_node.step],
                    keywords=[]
                )
            
            # Case 5: x[:] -> getFullCopy(x)
            elif slice_node.lower is None and slice_node.upper is None and slice_node.step is None:
                return ast.Call(
                    func=ast.Name(id="getFullCopy", ctx=ast.Load()),
                    args=[node.value],
                    keywords=[]
                )
        
        # Default case: x[i] -> getItem(x)(i)
        return ast.Call(
                func=ast.Call(
                    func=ast.Name(id="getItem", ctx=ast.Load()),
                    args=[node.value],
                    keywords=[]
                ),
                args=[node.slice],
                keywords=[]
            )
    
    def visit_Tuple(self, node):
        # Wrap the tuple elements in a call to a special function.
        new_node = ast.Call(
            func=ast.Name(id="__tuple__", ctx=ast.Load()),
            args=node.elts,
            keywords=[]
        )
        return ast.copy_location(new_node, node)

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        # Check if this constant is a string.
        if isinstance(node.value, str):
            # If the string is a valid identifier, use it as a Name;
            # otherwise, you might want to leave it unchanged or handle it specially.
            if node.value.isidentifier():
                new_arg = ast.Name(id=node.value, ctx=ast.Load())
            else:
                # Fall back to keeping it as a constant if it can't be an identifier.
                new_arg = node
            new_node = ast.Call(
                func=ast.Name(id="__str__", ctx=ast.Load()),
                args=[new_arg],
                keywords=[]
            )
            return ast.copy_location(new_node, node)
        else:
            return node
        
    def visit_Set(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Wrap the set elements in a call to __set__
        new_node = ast.Call(
            func=ast.Name(id="__set__", ctx=ast.Load()),
            args=node.elts,
            keywords=[]
        )
        return ast.copy_location(new_node, node)
    
    def visit_Dict(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Transform {k1: v1, k2: v2} into __dict__(__tuple__(k1, v1), __tuple__(k2, v2))
        pairs = []
        for key, value in zip(node.keys, node.values):
            # Create a __tuple__ function call for each key-value pair
            tuple_call = ast.Call(
                func=ast.Name(id="__tuple__", ctx=ast.Load()),
                args=[key, value],
                keywords=[]
            )
            pairs.append(tuple_call)
        
        # Create the call with the pairs as arguments
        new_node = ast.Call(
            func=ast.Name(id="__dict__", ctx=ast.Load()),
            args=pairs,
            keywords=[]
        )
        return ast.copy_location(new_node, node)
    
    def visit_Starred(self, node):
        # Process nested nodes first
        node = self.generic_visit(node)
        
        # Transform *expr into __star__(expr)
        return ast.Call(
            func=ast.Name(id="__star__", ctx=ast.Load()),
            args=[node.value],
            keywords=[]
        )
    
class GeneratorExpTransformer(ast.NodeTransformer):
    def visit_GeneratorExp(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Extract components: expression, target variable, and iterable
        expr = node.elt
        gen = node.generators[0]  # For simplicity, handle the first generator
        target = gen.target
        iterable = gen.iter
        
        # Create a __genExpr__ function call
        # __genExpr__(expr)(target)(iterable)(conditions...)
        result = ast.Call(
            func=ast.Name(id='__genExpr__', ctx=ast.Load()),
            args=[expr],
            keywords=[]
        )
        
        # Add the target variable
        result = ast.Call(
            func=result,
            args=[target],
            keywords=[]
        )
        
        # Add the iterable
        result = ast.Call(
            func=result, 
            args=[iterable],
            keywords=[]
        )
        
        # Add any filter conditions
        for if_condition in gen.ifs:
            result = ast.Call(
                func=result,
                args=[if_condition],
                keywords=[]
            )
            
        return ast.copy_location(result, node)

class MethodCallTransformer(ast.NodeTransformer):
    """
    Transform method calls like obj.method(args) into method(obj, args)
    Example: x32.index(x93) becomes index_M(x32, x93)
    """
    
    def visit_Call(self, node):
        # First process any nested elements
        node = self.generic_visit(node)
        
        # Check if the function being called is an attribute access (obj.method)
        if isinstance(node.func, ast.Attribute):
            # Extract the method name and object
            method_name = node.func.attr
            obj = node.func.value
            
            # Create a new function call: method(obj, *args)
            # Insert the object as the first argument
            return ast.Call(
                func=ast.Name(id=f"{method_name}_M", ctx=ast.Load()),
                args=[obj] + node.args,
                keywords=node.keywords
            )
        
        # For other calls, return unchanged
        return node

class NestedStructureTransformer(ast.NodeTransformer):
    """
    Post-processes the AST to ensure all nested structures are properly transformed.
    Runs after the standard transformers to catch any missed transformations.
    """
    
    def visit_Call(self, node):
        # Process the function and arguments first
        node = self.generic_visit(node)
        
        # Look specifically at function arguments for untransformed structures
        for i, arg in enumerate(node.args):
            # Check for untransformed tuples
            if isinstance(arg, ast.Tuple):
                node.args[i] = ast.Call(
                    func=ast.Name(id="__tuple__", ctx=ast.Load()),
                    args=arg.elts,
                    keywords=[]
                )
                ast.copy_location(node.args[i], arg)
            
            # Check for untransformed lists  
            elif isinstance(arg, ast.List):
                node.args[i] = ast.Call(
                    func=ast.Name(id="__list__", ctx=ast.Load()),
                    args=arg.elts,
                    keywords=[]
                )
                ast.copy_location(node.args[i], arg)
                
        # Check for lists in keywords that might need transformation
        for keyword in node.keywords:
            if isinstance(keyword.value, ast.Tuple):
                keyword.value = ast.Call(
                    func=ast.Name(id="__tuple__", ctx=ast.Load()),
                    args=keyword.value.elts,
                    keywords=[]
                )
                ast.copy_location(keyword.value, keyword.value)
                
            elif isinstance(keyword.value, ast.List):
                keyword.value = ast.Call(
                    func=ast.Name(id="__list__", ctx=ast.Load()),
                    args=keyword.value.elts,
                    keywords=[]
                )
                ast.copy_location(keyword.value, keyword.value)
                
        return node
    
    def visit_BinOp(self, node):
        # Check if this is a binary operation that needs transformation
        op_map = {
            ast.Add: "add",
            ast.Sub: "sub", 
            ast.Mult: "mul",
            ast.FloorDiv: "floordiv"
        }
        
        func_name = op_map.get(type(node.op))
        if func_name:
            return ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=[self.visit(node.left), self.visit(node.right)],
                keywords=[]
            )
        
        # If not a recognized operation, process children
        return self.generic_visit(node)



def transform_lambda_string(s):
    import re
    """
    Given a string with nested lambda expressions where each lambda has a single parameter,
    this function renames each lambda parameter (and all subsequent occurrences of that token)
    to a new name x1, x2, ... in the order the lambda declarations are encountered.
    
    Example:
      "lambda tp: lambda rp: (tp, rp, tp)"
    becomes:
      "lambda x1: lambda x2: (x1, x2, x1)"
    """
    # This regex matches either:
    #   - a lambda declaration: "lambda <word>:"
    #   - or any word token.
    # Using two capture groups:
    #   group(1): the variable name right after "lambda "
    #   group(2): any other word token.
    token_regex = re.compile(r"lambda\s+(\w+):|(\w+)")
    
    mapping = {}  # current mapping from original variable names to new names.
    counter = 1   # counter for naming (x1, x2, x3, …)
    result = []   # list to accumulate parts of the output string.
    last_end = 0  # track end of last match so we can copy non‐matched text.
    
    for match in token_regex.finditer(s):
        # Append any characters between the end of the previous match and the start of this one.
        result.append(s[last_end:match.start()])
        if match.group(1):  # This is a lambda declaration, e.g. "lambda tp:"
            orig_var = match.group(1)
            new_name = f"x{counter}"
            counter += 1
            # Update (or override) the mapping for this variable.
            mapping[orig_var] = new_name
            # Output the lambda keyword along with the new variable name and colon.
            result.append(f"lambda {new_name}:")
        elif match.group(2):  # This is a normal word token.
            word = match.group(2)
            # If this word has been bound in a lambda, replace it.
            if word in mapping:
                result.append(mapping[word])
            else:
                result.append(word)
        last_end = match.end()
    
    # Append any trailing text after the last match.
    result.append(s[last_end:])
    return "".join(result)

def transform_lambda(expr_str):
    """
    Applies the transformations to the input lambda expression.
    """
    # Parse the expression. We use mode='eval' because the input is a single expression.
    tree = ast.parse(expr_str, mode='eval')         
                                                    # ------------ Examples ------------
    tree = OperatorTransformer().visit(tree)        # 13+2                  -> add(13, 2)
    tree = BoolOpTransformer().visit(tree)          # x and y               -> andOp(x, y)
    tree = BitOpTransformer().visit(tree)           # x | y                 -> bitOr(x, y)
    tree = IfExpTransformer().visit(tree)           # if z then x else y    -> ifElse(z, x, y)
    tree = GeneratorExpTransformer().visit(tree)    # x for x in y if z     -> __genExpr__(x, x, y, z)
    tree = TaggerTransformer().visit(tree)          # [x, y]                -> __list__(x, y)
    tree = MethodCallTransformer().visit(tree)      # x.index(3)            -> index_M(x, 3)
    
    # Transform all nested structures
    tree = NestedStructureTransformer().visit(tree) # TODO: still misses elements e.g. strings nested in a tuple nested in a dictionary
                                                    # dict(__list__(__tuple__('input')(x19)) ... )

    tree = CurryTransformer().visit(tree)           # __genExpr__(z, x, y)  -> __genExpr__(z)(x)(y) 
    ast.fix_missing_locations(tree)
    
    # Convert the AST back into code
    new_expr = ast.unparse(tree)

    # Rename all variables bound by lambdas to x_i
    new_expr = transform_lambda_string(new_expr)    # lambda y: ... y ...   -> lambda x1: ... x1 ...

    return new_expr

def fix_lambda_tuple_params_ast(code_str):
    """
    Fix lambda expressions with tuple parameters using the AST module for more reliable parsing.
    """
    import ast
    import re
    
    # Use regex to find potential lambda expressions with tuple parameters
    lambda_pattern = r'lambda\s+[^:]*\([^)]+\)[^:]*:'
    lambda_matches = list(re.finditer(lambda_pattern, code_str))
    
    # If no potential matches, return the original string
    if not lambda_matches:
        return code_str
    
    # Process each match from end to beginning to avoid position shifts
    result = code_str
    for match in reversed(lambda_matches):
        start, end = match.span()
        lambda_expr = code_str[start:end]
        
        # Replace tuple parameters with flattened parameters
        fixed_lambda = re.sub(r'\(([^()]+)\)', r'\1', lambda_expr)
        result = result[:start] + fixed_lambda + result[end:]
    
    return result

# Example usage
if __name__ == "__main__":
    # Path to file that should be flattened
    # file_to_flatten_path = os.path.join("test_inputs", "ifs_test.py")

    generator_functions_dir = os.listdir(os.path.join("..", "reArc", "generator_functions"))
    # print(generator_functions_dir[0])
    # >> generate_b782dc8a.py
    file_to_flatten_path = os.path.join("..", "reArc", "generator_functions", f"{generator_functions_dir[0]}")

    # Flatten and display the python program
    test = Flatliner()
    test.set_ast(file_to_flatten_path)
    result = test.unparse()

    # result = "(lambda _Y: lambda diff_lb, diff_ub: (lambda cols: (lambda wall_pairs: (lambda dlt: (lambda walls: (lambda fullsucc: (lambda cc, cell, direc, dotcol, gi, go, grid, h, idx, kk, maze, nbhs, ncol, neighbour, next_cell, nobjs, nv, obj, obj1, obj2, objs, pathcol, row, stck, w, wallcol, x2, y2: (lambda _loop1: _loop1(cc, cell, direc, dotcol, gi, go, grid, h, idx, kk, maze, nbhs, ncol, neighbour, next_cell, nobjs, nv, obj, obj1, obj2, objs, pathcol, row, stck, w, wallcol, x2, y2))(_Y(lambda _loop1: (lambda cc, cell, direc, dotcol, gi, go, grid, h, idx, kk, maze, nbhs, ncol, neighbour, next_cell, nobjs, nv, obj, obj1, obj2, objs, pathcol, row, stck, w, wallcol, x2, y2: ((lambda h: (lambda w: (lambda maze: (lambda kk: (lambda stck: (lambda cc: (lambda nv: (lambda cc, direc, nbhs, neighbour, next_cell, nv, x2, y2: (lambda _loop5: _loop5(cc, direc, nbhs, neighbour, next_cell, nv, x2, y2))(_Y(lambda _loop5: (lambda cc, direc, nbhs, neighbour, next_cell, nv, x2, y2: ((lambda nbhs: (lambda _term6, _items6: (lambda _targ6: (lambda dx, dy, _targ6, direc, neighbour, x2, y2: (lambda _loop6: _loop6(dx, dy, _targ6, direc, neighbour, x2, y2))(_Y(lambda _loop6: (lambda dx, dy, _targ6, direc, neighbour, x2, y2: ([[((lambda neighbour: ([nbhs.append((direc, neighbour)), (lambda _targ6: _loop6(dx, dy, _targ6, direc, neighbour, x2, y2))(next(_items6, _term6))][-1] if all(neighbour['walls'].values()) else (lambda _targ6: _loop6(dx, dy, _targ6, direc, neighbour, x2, y2))(next(_items6, _term6))))(maze[x2][y2]) if (0 <= x2 < w) and (0 <= y2 < h) else (lambda _targ6: _loop6(dx, dy, _targ6, direc, neighbour, x2, y2))(next(_items6, _term6))) for (x2, y2) in [((cc['x'] + dx), (cc['y'] + dy))]][0] for (direc, dx, dy) in [_targ6]][0]) if (_targ6 is not _term6) else ((lambda cc: _loop5(cc, direc, nbhs, neighbour, next_cell, nv, x2, y2))(stck.pop()) if not nbhs else [[[[stck.append(cc), (lambda cc: (lambda nv: _loop5(cc, direc, nbhs, neighbour, next_cell, nv, x2, y2))((nv + 1)))(next_cell)][-1] for next_cell['walls'][wall_pairs[direc]] in [False]][0] for cc['walls'][direc] in [False]][0] for (direc, next_cell) in [choice(nbhs)]][0])))))(dx, dy if 'dx, dy' in dir() else None, _targ6 if '_targ6' in dir() else None, direc if 'direc' in dir() else None, neighbour if 'neighbour' in dir() else None, x2 if 'x2' in dir() else None, y2 if 'y2' in dir() else None))(next(_items6, _term6)))([], iter(dlt)))([])) if (nv < kk) else [(lambda grid: (lambda _term2, _items2: (lambda _targ2: (lambda _targ2, row, y: (lambda _loop2: _loop2(_targ2, row, y))(_Y(lambda _loop2: (lambda _targ2, row, y: ((lambda y: (lambda row: (lambda _term4, _items4: (lambda _targ4: (lambda _targ4, x: (lambda _loop4: _loop4(_targ4, x))(_Y(lambda _loop4: (lambda _targ4, x: ((lambda x: [row.append(wallcol), [row.append((pathcol if maze[x][y]['walls']['E'] else wallcol)), (lambda _targ4: _loop4(_targ4, x))(next(_items4, _term4))][-1]][-1])(_targ4)) if (_targ4 is not _term4) else [grid.append(row), (lambda row: (lambda _term3, _items3: (lambda _targ3: (lambda _targ3, x: (lambda _loop3: _loop3(_targ3, x))(_Y(lambda _loop3: (lambda _targ3, x: ((lambda x: [row.append((pathcol if maze[x][y]['walls']['S'] else wallcol)), [row.append(pathcol), (lambda _targ3: _loop3(_targ3, x))(next(_items3, _term3))][-1]][-1])(_targ3)) if (_targ3 is not _term3) else [grid.append(row), (lambda _targ2: _loop2(_targ2, row, y))(next(_items2, _term2))][-1]))))(_targ3 if '_targ3' in dir() else None, x if 'x' in dir() else None))(next(_items3, _term3)))([], iter(range(w))))([pathcol])][-1]))))(_targ4 if '_targ4' in dir() else None, x if 'x' in dir() else None))(next(_items4, _term4)))([], iter(range(w))))([pathcol]))(_targ2)) if (_targ2 is not _term2) else (lambda gi: (lambda objs: (lambda objs: (lambda objs: (_loop1(cc, cell, direc, dotcol, gi, go, grid, h, idx, kk, maze, nbhs, ncol, neighbour, next_cell, nobjs, nv, obj, obj1, obj2, objs, pathcol, row, stck, w, wallcol, x2, y2) if (len(objs) == 0) else (lambda objs: (lambda nobjs: (lambda idx: (lambda obj: (lambda cell: (lambda gi: (lambda nbhs: (lambda gi: (lambda obj1: (lambda obj2: (lambda go: (lambda go: (lambda rotf: (lambda gi: (lambda go: {'input': gi, 'output': go})(rotf(go)))(rotf(gi)))(choice((identity, rot90, rot180, rot270))))(fill(go, ncol, obj2)))(fill(gi, dotcol, obj1)))((obj - obj1)))(sfilter(obj, lambda ij: even(manhattan({ij}, {cell})))))(fill(gi, ncol, nbhs)))((dneighbors(cell) & ofcolor(gi, pathcol))))(fill(gi, dotcol, {cell})))(choice(totuple(obj))))(toindices(objs[idx])))(unifint(diff_lb, diff_ub, (0, (nobjs - 1)))))(len(objs)))(order(objs, size))))(sfilter(objs, lambda obj: size(obj) > 4)))(colorfilter(objs, pathcol)))(objects(gi, T, F, F)))(tuple((tuple(r[1:-1]) for r in grid[1:-1])))))))(_targ2 if '_targ2' in dir() else None, row if 'row' in dir() else None, y if 'y' in dir() else None))(next(_items2, _term2)))([], iter(range(h))))([[pathcol for x in range(w * 2)]]) for (pathcol, wallcol, dotcol, ncol) in [sample(cols, 4)]][0]))))(cc if 'cc' in dir() else None, direc if 'direc' in dir() else None, nbhs if 'nbhs' in dir() else None, neighbour if 'neighbour' in dir() else None, next_cell if 'next_cell' in dir() else None, nv if 'nv' in dir() else None, x2 if 'x2' in dir() else None, y2 if 'y2' in dir() else None))(1))(maze[0][0]))([]))((h * w)))([[{'x': x, 'y': y, 'walls': {**walls}} for y in range(h)] for x in range(w)]))(unifint(diff_lb, diff_ub, (3, 15))))(unifint(diff_lb, diff_ub, (3, 15)))) if True else (lambda rotf: (lambda gi: (lambda go: {'input': gi, 'output': go})(rotf(go)))(rotf(gi)))(choice((identity, rot90, rot180, rot270)))))))(cc if 'cc' in dir() else None, cell if 'cell' in dir() else None, direc if 'direc' in dir() else None, dotcol if 'dotcol' in dir() else None, gi if 'gi' in dir() else None, go if 'go' in dir() else None, grid if 'grid' in dir() else None, h if 'h' in dir() else None, idx if 'idx' in dir() else None, kk if 'kk' in dir() else None, maze if 'maze' in dir() else None, nbhs if 'nbhs' in dir() else None, ncol if 'ncol' in dir() else None, neighbour if 'neighbour' in dir() else None, next_cell if 'next_cell' in dir() else None, nobjs if 'nobjs' in dir() else None, nv if 'nv' in dir() else None, obj if 'obj' in dir() else None, obj1 if 'obj1' in dir() else None, obj2 if 'obj2' in dir() else None, objs if 'objs' in dir() else None, pathcol if 'pathcol' in dir() else None, row if 'row' in dir() else None, stck if 'stck' in dir() else None, w if 'w' in dir() else None, wallcol if 'wallcol' in dir() else None, x2 if 'x2' in dir() else None, y2 if 'y2' in dir() else None))(False))({'N': True, 'S': True, 'E': True, 'W': True}))([('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1)), ('N', (0, -1))]))({'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}))(interval(0, 10, 1)))((lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))))"

    # result = fix_lambda_tuple_params_ast(result)
    print(f"Original result:\n{result}")

    # Transform the lambda expression
    result_transformed = transform_lambda(result)
    print(f"Transformed result:\n{result_transformed}")

