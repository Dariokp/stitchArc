from pprint import pprint
import ast
import re
import numpy as np
from copy import deepcopy


def parse(expr):
    tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
    def read_from_tokens(tokens):
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF')
        token = tokens.pop(0)
        if token == '(':
            L = []
            while tokens[0] != ')':
                L.append(read_from_tokens(tokens))
            tokens.pop(0)  # pop off ')'
            return L
        elif token == ')':
            raise SyntaxError('unexpected )')
        else:
            return token
    return read_from_tokens(tokens)


def generate_python_code(expression):
    if isinstance(expression, list):
        if len(expression) == 1:
            return generate_python_code(expression[0])
        else:
            args_strings = f'{generate_python_code(expression[0])}'
            for x in expression[1:]:
                args_strings += f'({generate_python_code(x)})'
            return args_strings
    else:
        return str(expression)


def translate(text, conversion_dict, before=None):
    """
    Translate words from a text using a conversion dictionary

    Arguments:
        text: the text to be translated
        conversion_dict: the conversion dictionary
        before: a function to transform the input
        (by default it will to a lowercase)
    """
    # if empty:
    if not text: return text
    # preliminary transformation:
    before = before or str.lower
    t = before(text)
    for key, value in conversion_dict.items():
        t = t.replace(key, value)
    return t


def add_variables(formula, varstitch, varpython, variables=None):
    """
    stitch uses De Bruijn variables, but python
    needs explicit variables after lambdas. 
    This takes a parsed formula (recursive list of lists format)
    and adds the variables explicitly to lambdas.
    """
    if variables is None:
        variables = []
    if isinstance(formula, list):
        operator, *arguments = formula
        if operator=="lam":
            newvar = f"{varpython}{len(variables)+1}"
            operator = f"lambda {newvar}: "
            variables = [newvar] + variables
        return [
            operator, 
            *[
                add_variables(
                    x,
                    variables=variables,
                    varstitch=varstitch, 
                    varpython=varpython,
                )
                for x in arguments
            ]
        ]
    elif isinstance(formula, str) and formula.startswith(varstitch):
        return variables[int(formula[1:])]
    else:
        return formula


def stitch_to_python(expr, primitive_replacements=None, 
                     varstitch='$', varpython='x'):
    if primitive_replacements is None:
        primitive_replacements = dict()
    expr = translate(
        expr, 
        primitive_replacements
    )
    expr = parse(expr)
    expr = add_variables(
        expr, 
        varstitch=varstitch,
        varpython=varpython,
        variables=[f"x{i}" for i in range(100)]
    )
    expr = generate_python_code(expr)
    return expr


def abstraction_to_python(a):
    """
    convert from stitch found abstraction
    to abstraction in python notation
    """
    a = a.split(':=')[1].strip()
    a = a.replace('#', 'y')
    indices_vars = list(map(
        int, 
        re.findall(
            r'(?<=y)[\d]+',
            a
        )
    ))
    prefix = ''
    if len(indices_vars) > 0:
        var_max = max(indices_vars)
        prefix = ''.join([
            f'lambda y{i}: '
            for i in range(var_max+1)
        ])
    return prefix + stitch_to_python(a)

stitchExpr = "(lam (lam (lam (lam (lam (lam (lam (lam (lam (lam (__ifExp__ (__and__ (eq $1 $0) (eq $0 1)) (__getitem__ (__listComp__ (lam (lam (lam (lam (lam (lam (lam (lam (lam (lam (dict (__list__ (__tuple__ (__str__ input) $1) (__tuple__ (__str__ output) $0))) (x18 $0)) (x18 $0)) (choice (__tuple__ identity rot90 rot180 rot270))) (fill $36 2 (product $5 $6))) (fill (canvas $2 (__tuple__ $11 $10)) $1 $3)) (choice (remove $1 $11))) (choice $10)) (combine (apply (lbind astuple 0) $2) (apply (rbind astuple (sub $7 1)) $1))) (sample (interval 1 $7 1) $2)) (sample (interval 0 (sub $5 1) 1) $2)) (__tuple__ $1 $0) (__list__ (sample (__list__ 1 2) 2))) 0) (lam (lam (lam (lam (lam (lam (lam (lam (lam (lam (dict (__list__ (__tuple__ (__str__ input) $1) (__tuple__ (__str__ output) $0))) (x28 $0)) (x28 $0)) (choice (__tuple__ identity rot90 rot180 rot270))) (fill $46 2 (product $5 $6))) (fill (canvas $2 (__tuple__ $11 $10)) $1 $3)) (choice (remove $1 $11))) (choice $10)) (combine (apply (lbind astuple 0) $2) (apply (rbind astuple (sub $7 1)) $1))) (sample (interval 1 $7 1) $2)) (sample (interval 0 (sub $5 1) 1) $2))) (unifint $9 $8 $3)) (unifint $8 $7 $1)) (__tuple__ 1 (add (floordiv $2 2) 1))) (__tuple__ 1 (add (floordiv $2 2) 1))) (unifint $5 $4 $3)) (unifint $4 $3 $2)) (remove 2 (interval 0 10 1))) (__tuple__ 3 30))))"
result = stitch_to_python(stitchExpr)
print(result)