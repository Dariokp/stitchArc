import ast
import re
import numpy as np
from copy import deepcopy

import os

def remove_variables(formula, varstitch, varpython, variables=None):
    if variables is None:
        variables = []

    if isinstance(formula, list):
        # structure is [[fname arg1], arg2]]
        if isinstance(formula[0], list):
            return remove_variables(
                [*formula[0], *formula[1:]],
                variables=variables,
                varstitch=varstitch, 
                varpython=varpython, 
            )
        else:
            operator, *arguments = formula
            if operator.replace(' ', '').startswith('lambda:'):
                # if there is a lambda with
                # 0 arguments, do not add
                # a variable
                assert len(arguments)==1
                return remove_variables(
                    arguments[0],
                    variables=variables,
                    varstitch=varstitch, 
                    varpython=varpython, 
                )
            elif operator.startswith("lambda"):
                newvar = operator.strip()[:-1].split()[1]
                operator = f"lam "
                variables = [newvar] + variables
            return [
                operator, 
                *[
                    remove_variables(
                        x,
                        variables=variables,
                        varstitch=varstitch, 
                        varpython=varpython, 
                    )
                    for x in arguments
                ]
            ]
    # variable!
    elif isinstance(formula, str) and formula.startswith(varpython):
        # return variables[int(formula[1:])]
        return f'{varstitch}{variables.index(formula)}'
    # function name or argument name!
    else:
        return formula


def visit_node(node):
    """
    Visit AST node and return appropriate value.
    """
    if isinstance(node, ast.Call):
        func_name = visit_node(node.func)
        args = [visit_node(arg) for arg in node.args]
        return [func_name] + args
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Lambda):
        return [f'lambda {", ".join([arg.arg for arg in node.args.args])}:', visit_node(node.body)]
    elif isinstance(node, ast.Constant):
        return str(node.value)
    elif isinstance(node, ast.UnaryOp):
        # Handle negative numbers
        if isinstance(node.op, ast.USub):
            operand = visit_node(node.operand)
            # If operand is a simple number, just prepend the minus sign
            if isinstance(node.operand, ast.Constant) and isinstance(node.operand.value, (int, float)):
                return f"-{operand}"
            # Otherwise treat it as a function call
            else:
                return ["neg", operand]
        # else:
        #     # Handle other unary operators if needed
        #     op_map = {ast.UAdd: "pos", ast.Not: "not", ast.Invert: "~"}
        #     op_name = op_map.get(type(node.op), "unknown_op")
        #     return [op_name, visit_node(node.operand)]

    else:
        raise ValueError(f"Unhandled node type: {type(node)}")


def parse_function_calls(expression):
    """
    Parse function call expressions into nested list of function names and arguments.
    """
    parsed_expression = ast.parse(expression, mode='eval')
    return visit_node(parsed_expression.body)
    

def parsed_to_stitch(parsed):
    if isinstance(parsed, list):
        op, *args = parsed
        return f'({op.strip()} {" ".join([parsed_to_stitch(x) for x in args])})'
    else:
        return str(parsed)


def python_to_stitch(expr, varstitch='$', varpython='x'):
    return parsed_to_stitch(
        remove_variables(
            parse_function_calls(
                expr
            ),
            varstitch=varstitch,
            varpython=varpython,
            variables=[f"x{i}" for i in range(400)]
        )
    )

function_to_be_flattened_path = os.path.join("re-arc", "re-arc_generator.py")

# pythonExpr = "lambda x1: lambda x2: lambda x3: lambda x4: lambda x5: lambda x6: (lambda x7: (lambda x8: (lambda x9: (lambda x10: dict(__list__(__tuple__(__str__(input))(x9))(__tuple__(__str__(output))(x10))))(x8(x10)))(x8(x9)))(choice(__tuple__(identity)(rot90)(rot180)(rot270))))(fill(x9)(2)(product(x2)(x1)))"
# pythonExpr = "lambda x1: lambda x2: (lambda x3: (lambda x4: (lambda x5: (lambda x6: (lambda x7: (lambda x8: (lambda x9: (lambda x10: __ifExp__(__and__(eq(x9)(x10))(eq(x10)(1)))(__getitem__(__listComp__((lambda x11: (lambda x12: (lambda x13: (lambda x14: (lambda x15: (lambda x16: (lambda x17: (lambda x18: (lambda x19: (lambda x20: dict(__list__(__tuple__(__str__(input))(x19))(__tuple__(__str__(output))(x20))))(x18(x20)))(x18(x19)))(choice(__tuple__(identity)(rot90)(rot180)(rot270))))(fill(x19)(2)(product(x12)(x11))))(fill(canvas(x14)(__tuple__(x5)(x6)))(x15)(x13)))(choice(remove(x14)(x4))))(choice(x4)))(combine(apply(lbind(astuple)(0))(x11))(apply(rbind(astuple)(sub(x6)(1)))(x12))))(sample(interval(1)(x5)(1))(x10)))(sample(interval(0)(sub(x6)(1))(1))(x9)))(__tuple__(x9)(x10))(__list__(sample([1, 2])(2))))(0))((lambda x21: (lambda x22: (lambda x23: (lambda x24: (lambda x25: (lambda x26: (lambda x27: (lambda x28: (lambda x29: (lambda x30: dict(__list__(__tuple__(__str__(input))(x29))(__tuple__(__str__(output))(x30))))(x28(x30)))(x28(x29)))(choice(__tuple__(identity)(rot90)(rot180)(rot270))))(fill(x29)(2)(product(x22)(x21))))(fill(canvas(x24)(__tuple__(x5)(x6)))(x25)(x23)))(choice(remove(x24)(x4))))(choice(x4)))(combine(apply(lbind(astuple)(0))(x21))(apply(rbind(astuple)(sub(x6)(1)))(x22))))(sample(interval(1)(x5)(1))(x10)))(sample(interval(0)(sub(x6)(1))(1))(x9))))(unifint(x1)(x2)(x7)))(unifint(x1)(x2)(x8)))(__tuple__(1)(add(floordiv(x6)(2))(1))))(__tuple__(1)(add(floordiv(x5)(2))(1))))(unifint(x1)(x2)(x3)))(unifint(x1)(x2)(x3)))(remove(2)(interval(0)(10)(1))))(__tuple__(3)(30))"
# pythonExpr = "lambda x1: lambda x2: (lambda x3: (lambda x4: (lambda x5: (lambda x6: (lambda x7: (lambda x8: (lambda x9: (lambda x10: __ifExp__(__and__(eq(x9)(x10))(eq(x10)(1)))(__getitem__(__listComp__((lambda x11: (lambda x12: (lambda x13: (lambda x14: (lambda x15: (lambda x16: (lambda x17: (lambda x18: (lambda x19: (lambda x20: dict(__list__(__tuple__(__str__(input))(x19))(__tuple__(__str__(output))(x20))))(x18(x20)))(x18(x19)))(choice(__tuple__(identity)(rot90)(rot180)(rot270))))(fill(x19)(2)(product(x12)(x11))))(fill(canvas(x14)(__tuple__(x5)(x6)))(x15)(x13)))(choice(remove(x14)(x4))))(choice(x4)))(combine(apply(lbind(astuple)(0))(x11))(apply(rbind(astuple)(sub(x6)(1)))(x12))))(sample(interval(1)(x5)(1))(x10)))(sample(interval(0)(sub(x6)(1))(1))(x9)))(__tuple__(x9)(x10))(__list__(sample(__list__(1)(2))(2))))(0))((lambda x21: (lambda x22: (lambda x23: (lambda x24: (lambda x25: (lambda x26: (lambda x27: (lambda x28: (lambda x29: (lambda x30: dict(__list__(__tuple__(__str__(input))(x29))(__tuple__(__str__(output))(x30))))(x28(x30)))(x28(x29)))(choice(__tuple__(identity)(rot90)(rot180)(rot270))))(fill(x29)(2)(product(x22)(x21))))(fill(canvas(x24)(__tuple__(x5)(x6)))(x25)(x23)))(choice(remove(x24)(x4))))(choice(x4)))(combine(apply(lbind(astuple)(0))(x21))(apply(rbind(astuple)(sub(x6)(1)))(x22))))(sample(interval(1)(x5)(1))(x10)))(sample(interval(0)(sub(x6)(1))(1))(x9))))(unifint(x1)(x2)(x7)))(unifint(x1)(x2)(x8)))(__tuple__(1)(add(floordiv(x6)(2))(1))))(__tuple__(1)(add(floordiv(x5)(2))(1))))(unifint(x1)(x2)(x3)))(unifint(x1)(x2)(x3)))(remove(2)(interval(0)(10)(1))))(__tuple__(3)(30))"
# pythonExpr = "lambda x: lambda x1: (rotf(x))(choice(__tuple__(identity)(rot90)(rot180)(rot270)))(rotf(x1))"
# pythonExpr = "lambda x1: lambda x2: dict(__list__(__tuple__('input')(x1), __tuple__('output')(x2)))"
# pythonExpr = "lambda x10: foo(x10)"

# pythonExpr = "(lambda x1: lambda x2: lambda x3: (lambda x4: (lambda x5: (lambda x6: (lambda x7: (lambda x8: (lambda x9: (lambda x10: (lambda x11: (lambda x12: (lambda x13: (lambda x14: (lambda x15: (lambda x16: lambda x17: (lambda x18: (lambda x19: lambda x20: lambda x21: lambda x22: (lambda x23: x23(x19)(x20)(x21)(x22))(x1(lambda x24: lambda x25: lambda x26: lambda x27: lambda x28: ifElse(isnot(x25)(x16))((lambda x29: ifElse(eq(len(x28))(0))((lambda x30: (lambda x31: (lambda x32: (lambda x33: (lambda x34: lambda x35: (lambda x36: (lambda x37: lambda x38: lambda x39: lambda x40: (lambda x41: x41(x37)(x38)(x39)(x40))(x1(lambda x42: lambda x43: lambda x44: lambda x45: lambda x46: ifElse(isnot(x43)(x34))(getItem(__listComp__((lambda x47: (lambda x48: x42(x48)(x44)(x47)(x46))(next(x35)(x34)))(fill(x47)(x44)(connect(__tuple__(0)(x46))(__tuple__(sub(x5)(1))(x46)))))(__tuple__(x46)(x44))(__list__(x48)))(0))((lambda x49: (lambda x50: (lambda x51: (lambda x52: (lambda x53: lambda x54: (lambda x55: (lambda x56: lambda x57: lambda x58: lambda x59: lambda x60: lambda x61: lambda x62: lambda x63: lambda x64: (lambda x65: x65(x56)(x57)(x58)(x59)(x60)(x61)(x62)(x63)(x64))(x1(lambda x66: lambda x67: lambda x68: lambda x69: lambda x70: lambda x71: lambda x72: lambda x73: lambda x74: lambda x75: ifElse(isnot(x67)(x53))((lambda x76: (lambda x77: (lambda x78: (lambda x79: (lambda x80: lambda x81: (lambda x82: (lambda x83: lambda x84: lambda x85: lambda x86: lambda x87: lambda x88: lambda x89: (lambda x90: x90(x83)(x84)(x85)(x86)(x87)(x88)(x89))(x1(lambda x91: lambda x92: lambda x93: lambda x94: lambda x95: lambda x96: lambda x97: lambda x98: ifElse(isnot(x92)(x80))(getItem(__listComp__((lambda x99: ifElse(elem(x93)(x32))((lambda x100: (lambda x101: ifElse(gt(x94)(x101))((lambda x102: (lambda x103: x91(x103)(x93)(x94)(x99)(x102)(x100)(x101))(next(x81)(x80)))(fill(x102)(x93)(__set__(__tuple__(x76)(add(x101)(1))))))((lambda x104: (lambda x105: x91(x105)(x93)(x94)(x99)(x104)(x100)(x101))(next(x81)(x80)))(fill(x104)(x93)(__set__(__tuple__(x76)(sub(x101)(1)))))))(getItem(x30)(x100)))(index_M(x32)(x93)))((lambda x106: x91(x106)(x93)(x94)(x99)(x104)(x100)(x101))(next(x81)(x80))))(fill(x99)(x93)(__set__(__tuple__(x76)(x94)))))(__tuple__(x94)(x93))(__list__(x106)))(0))((lambda x107: x66(x107)(x79)(x78)(x99)(x104)(x100)(x76)(x101)(x77))(next(x54)(x53))))))(ifElse(elem(__str__(x106))(dir()))(x106)(None))(ifElse(elem(__str__(x93))(dir()))(x93)(None))(ifElse(elem(__str__(x94))(dir()))(x94)(None))(ifElse(elem(__str__(x99))(dir()))(x99)(None))(ifElse(elem(__str__(x104))(dir()))(x104)(None))(ifElse(elem(__str__(x100))(dir()))(x100)(None))(ifElse(elem(__str__(x101))(dir()))(x101)(None)))(next(x81)(x80)))(__list__())(iter(zip(x78)(x79))))(sample(totuple(bitOr(set(x32))(set(x13))))(x77)))(sample(x52)(x77)))(unifint(x2)(x3)(__tuple__(1)(min(add(x31)(x12))(sub(floordiv(sub(x6)(x31))(2))(1))))))(x107))(ifElse(choice(__tuple__(True)(False)))((lambda x108: (lambda x109: __dict__(__tuple__(__str__(input))(x108))(__tuple__(__str__(output))(x109)))(dmirror(x109)))(dmirror(x108)))(__dict__(__tuple__(__str__(input))(x108))(__tuple__(__str__(output))(x109)))))))(ifElse(elem(__str__(x107))(dir()))(x107)(None))(ifElse(elem(__str__(x79))(dir()))(x79)(None))(ifElse(elem(__str__(x78))(dir()))(x78)(None))(ifElse(elem(__str__(x108))(dir()))(x108)(None))(ifElse(elem(__str__(x109))(dir()))(x109)(None))(ifElse(elem(__str__(x100))(dir()))(x100)(None))(ifElse(elem(__str__(x76))(dir()))(x76)(None))(ifElse(elem(__str__(x101))(dir()))(x101)(None))(ifElse(elem(__str__(x77))(dir()))(x77)(None)))(next(x54)(x53)))(__list__())(iter(x51)))(difference(interval(0)(x6)(1))(x30)))(sample(interval(0)(x5)(1))(x50)))(unifint(x2)(x3)(__tuple__(1)(x5))))(tuple(__genExpr__(e)(e)(x108)))))))(ifElse(elem(__str__(x48))(dir()))(x48)(None))(ifElse(elem(__str__(x93))(dir()))(x93)(None))(ifElse(elem(__str__(x108))(dir()))(x108)(None))(ifElse(elem(__str__(x46))(dir()))(x46)(None)))(next(x35)(x34)))(__list__())(iter(zip(x30)(x32))))(canvas(x7)(__tuple__(x5)(x6))))(getItemUpTo(x32)(x31)))(len(x30)))(sorted(x30)))((lambda x110: (lambda x111: getItem(__list__(append_M(x30)(x110))((lambda x112: x24(x112)(x29)(x110)(x111))(next(x17)(x16))))(-1))(difference(x111)(interval(sub(x110)(2))(add(x110)(3))(1))))(choice(x111))))(x112))((lambda x113: (lambda x114: (lambda x115: (lambda x116: (lambda x117: lambda x118: (lambda x119: (lambda x120: lambda x121: lambda x122: lambda x123: (lambda x124: x124(x120)(x121)(x122)(x123))(x1(lambda x125: lambda x126: lambda x127: lambda x128: lambda x129: ifElse(isnot(x126)(x117))(getItem(__listComp__((lambda x130: (lambda x131: x125(x131)(x127)(x130)(x129))(next(x118)(x117)))(fill(x130)(x127)(connect(__tuple__(0)(x129))(__tuple__(sub(x5)(1))(x129)))))(__tuple__(x129)(x127))(__list__(x131)))(0))((lambda x132: (lambda x133: (lambda x134: (lambda x135: (lambda x136: lambda x137: (lambda x138: (lambda x139: lambda x140: lambda x141: lambda x142: lambda x143: lambda x144: lambda x145: lambda x146: lambda x147: (lambda x148: x148(x139)(x140)(x141)(x142)(x143)(x144)(x145)(x146)(x147))(x1(lambda x149: lambda x150: lambda x151: lambda x152: lambda x153: lambda x154: lambda x155: lambda x156: lambda x157: lambda x158: ifElse(isnot(x150)(x136))((lambda x159: (lambda x160: (lambda x161: (lambda x162: (lambda x163: lambda x164: (lambda x165: (lambda x166: lambda x167: lambda x168: lambda x169: lambda x170: lambda x171: lambda x172: (lambda x173: x173(x166)(x167)(x168)(x169)(x170)(x171)(x172))(x1(lambda x174: lambda x175: lambda x176: lambda x177: lambda x178: lambda x179: lambda x180: lambda x181: ifElse(isnot(x175)(x163))(getItem(__listComp__((lambda x182: ifElse(elem(x176)(x115))((lambda x183: (lambda x184: ifElse(gt(x177)(x184))((lambda x185: (lambda x186: x174(x186)(x176)(x177)(x182)(x185)(x183)(x184))(next(x164)(x163)))(fill(x185)(x176)(__set__(__tuple__(x159)(add(x184)(1))))))((lambda x187: (lambda x188: x174(x188)(x176)(x177)(x182)(x187)(x183)(x184))(next(x164)(x163)))(fill(x187)(x176)(__set__(__tuple__(x159)(sub(x184)(1)))))))(getItem(x113)(x183)))(index_M(x115)(x176)))((lambda x189: x174(x189)(x176)(x177)(x182)(x187)(x183)(x184))(next(x164)(x163))))(fill(x182)(x176)(__set__(__tuple__(x159)(x177)))))(__tuple__(x177)(x176))(__list__(x189)))(0))((lambda x190: x149(x190)(x162)(x161)(x182)(x187)(x183)(x159)(x184)(x160))(next(x137)(x136))))))(ifElse(elem(__str__(x189))(dir()))(x189)(None))(ifElse(elem(__str__(x176))(dir()))(x176)(None))(ifElse(elem(__str__(x177))(dir()))(x177)(None))(ifElse(elem(__str__(x182))(dir()))(x182)(None))(ifElse(elem(__str__(x187))(dir()))(x187)(None))(ifElse(elem(__str__(x183))(dir()))(x183)(None))(ifElse(elem(__str__(x184))(dir()))(x184)(None)))(next(x164)(x163)))(__list__())(iter(zip(x161)(x162))))(sample(totuple(bitOr(set(x115))(set(x13))))(x160)))(sample(x135)(x160)))(unifint(x2)(x3)(__tuple__(1)(min(add(x114)(x12))(sub(floordiv(sub(x6)(x114))(2))(1))))))(x190))(ifElse(choice(__tuple__(True)(False)))((lambda x191: (lambda x192: __dict__(__tuple__(__str__(input))(x191))(__tuple__(__str__(output))(x192)))(dmirror(x192)))(dmirror(x191)))(__dict__(__tuple__(__str__(input))(x191))(__tuple__(__str__(output))(x192)))))))(ifElse(elem(__str__(x190))(dir()))(x190)(None))(ifElse(elem(__str__(x162))(dir()))(x162)(None))(ifElse(elem(__str__(x161))(dir()))(x161)(None))(ifElse(elem(__str__(x191))(dir()))(x191)(None))(ifElse(elem(__str__(x192))(dir()))(x192)(None))(ifElse(elem(__str__(x183))(dir()))(x183)(None))(ifElse(elem(__str__(x159))(dir()))(x159)(None))(ifElse(elem(__str__(x184))(dir()))(x184)(None))(ifElse(elem(__str__(x160))(dir()))(x160)(None)))(next(x137)(x136)))(__list__())(iter(x134)))(difference(interval(0)(x6)(1))(x113)))(sample(interval(0)(x5)(1))(x133)))(unifint(x2)(x3)(__tuple__(1)(x5))))(tuple(__genExpr__(e)(e)(x191)))))))(ifElse(elem(__str__(x131))(dir()))(x131)(None))(ifElse(elem(__str__(x176))(dir()))(x176)(None))(ifElse(elem(__str__(x191))(dir()))(x191)(None))(ifElse(elem(__str__(x129))(dir()))(x129)(None)))(next(x118)(x117)))(__list__())(iter(zip(x113)(x115))))(canvas(x7)(__tuple__(x5)(x6))))(getItemUpTo(x115)(x114)))(len(x113)))(sorted(x113))))))(ifElse(elem(__str__(x112))(dir()))(x112)(None))(ifElse(elem(__str__(x29))(dir()))(x29)(None))(ifElse(elem(__str__(x129))(dir()))(x129)(None))(ifElse(elem(__str__(x111))(dir()))(x111)(None)))(next(x17)(x16)))(__list__())(iter(range(x114))))(__list__()))(interval(0)(x6)(1)))(sample(x11)(x12)))(unifint(x2)(x3)(__tuple__(0)(len(x11)))))(difference(x11)(x115)))(sample(x11)(x114)))(unifint(x2)(x3)(__tuple__(1)(floordiv(x6)(5)))))(remove(x7)(x4)))(choice(x4)))(unifint(x2)(x3)(__tuple__(8)(30))))(unifint(x2)(x3)(__tuple__(8)(30))))(interval(0)(10)(1)))(lambda x193: (lambda x194: x194(x194))(lambda x195: x193(lambda x196: x195(x195)(__star__(x196)))))"
# pythonExpr = "lambda x1: lambda x2: (lambda x3: (lambda x4: (lambda x5: (lambda x6: (lambda x7: (lambda x8: (lambda x9: (lambda x10: ifElse(fand(eq(x9)(x10))(eq(x10)(1)))(getItem(__listComp__((lambda x11: (lambda x12: (lambda x13: (lambda x14: (lambda x15: (lambda x16: (lambda x17: (lambda x18: (lambda x19: (lambda x20: dict(__list__(__tuple__('input')(x19))(__tuple__('output')(x20))))(x18(x20)))(x18(x19)))(choice(__tuple__(identity)(rot90)(rot180)(rot270))))(fill(x19)(2)(product(x12)(x11))))(fill(canvas(x14)(__tuple__(x5)(x6)))(x15)(x13)))(choice(remove(x14)(x4))))(choice(x4)))(combine(apply(lbind(astuple)(0))(x11))(apply(rbind(astuple)(sub(x6)(1)))(x12))))(sample(interval(1)(x5)(1))(x10)))(sample(interval(0)(sub(x6)(1))(1))(x9)))(__tuple__(x9)(x10))(__list__(sample(__list__(1)(2))(2))))(0))((lambda x21: (lambda x22: (lambda x23: (lambda x24: (lambda x25: (lambda x26: (lambda x27: (lambda x28: (lambda x29: (lambda x30: dict(__list__(__tuple__('input')(x29))(__tuple__('output')(x30))))(x28(x30)))(x28(x29)))(choice(__tuple__(identity)(rot90)(rot180)(rot270))))(fill(x29)(2)(product(x22)(x21))))(fill(canvas(x24)(__tuple__(x5)(x6)))(x25)(x23)))(choice(remove(x24)(x4))))(choice(x4)))(combine(apply(lbind(astuple)(0))(x21))(apply(rbind(astuple)(sub(x6)(1)))(x22))))(sample(interval(1)(x5)(1))(x10)))(sample(interval(0)(sub(x6)(1))(1))(x9))))(unifint(x1)(x2)(x7)))(unifint(x1)(x2)(x8)))(__tuple__(1)(add(floordiv(x6)(2))(1))))(__tuple__(1)(add(floordiv(x5)(2))(1))))(unifint(x1)(x2)(x3)))(unifint(x1)(x2)(x3)))(remove(2)(interval(0)(10)(1))))(__tuple__(3)(30))"
# pythonExpr = "(lambda x1: lambda x2: lambda x3: (lambda x4: (lambda x5: (lambda x6: (lambda x7: (lambda x8: (lambda x9: (lambda x10: (lambda x11: (lambda x12: (lambda x13: (lambda x14: (lambda x15: (lambda x16: lambda x17: lambda x18: lambda x19: lambda x20: lambda x21: lambda x22: lambda x23: lambda x24: lambda x25: lambda x26: lambda x27: lambda x28: lambda x29: lambda x30: lambda x31: (lambda x32: x32(x16)(x17)(x18)(x19)(x20)(x21)(x22)(x23)(x24)(x25)(x26)(x27)(x28)(x29)(x30)(x31))(x1(lambda x33: lambda x34: lambda x35: lambda x36: lambda x37: lambda x38: lambda x39: lambda x40: lambda x41: lambda x42: lambda x43: lambda x44: lambda x45: lambda x46: lambda x47: lambda x48: lambda x49: ifElse(andOp(lt(x48)(x10))(lte(x49)(x12)))(ifElse(orOp(eq(len(x46))(0))(eq(len(x39))(0)))((lambda x50: __dict__(__tuple__(__str__(input))(x38))(__tuple__(__str__(output))(x50)))(canvas(x44)(__tuple__(1)(1))))((lambda x51: (lambda x52: (lambda x53: ifElse(eq(len(x53))(0))((lambda x54: x33(x34)(x35)(x36)(x37)(x38)(x39)(x40)(x41)(x42)(x51)(x44)(x52)(x46)(x53)(x48)(x54))(add(x54)(1)))(getItem(__listComp__((lambda x55: (lambda x56: (lambda x57: ifElse(issubset_M(x56)(x39))((lambda x58: (lambda x59: (lambda x60: (lambda x61: ifElse(isComp(x44)(None))((lambda x62: (lambda x63: (lambda x64: (lambda x65: (lambda x66: x33(x56)(x64)(x63)(x57)(x65)(x61)(x40)(x41)(x55)(x51)(x62)(x52)(x58)(x53)(x60)(x66))(add(x66)(1)))(fill(x65)(x7)(x64)))(backdrop(ifElse(gt(len(x63))(2))(frozenset(sample(x63)(2)))(frozenset(x63)))))(totuple(backdrop(inbox(x56)))))(x57))((lambda x67: x33(x56)(x64)(x63)(x57)(x65)(x61)(x40)(x41)(x55)(x51)(x62)(x52)(x58)(x53)(x60)(x67))(add(x67)(1))))(sub(x61)(x56)))(add(x60)(1)))(fill(x65)(x57)(x56)))(remove(x57)(x58)))((lambda x68: x33(x56)(x64)(x63)(x57)(x65)(x61)(x40)(x41)(x55)(x51)(x62)(x52)(x58)(x53)(x60)(x68))(add(x68)(1))))(choice(x58)))(backdrop(x55)))(frozenset(__set__(__tuple__(x40)(x41))(__tuple__(sub(add(x40)(x51))(1))(sub(add(x41)(x52))(1))))))(__tuple__(x40)(x41))(__list__(choice(x53))))(0)))(totuple(sfilter(x61)(lambda x69: andOp(lt(getItem(x69)(0))(sub(x5)(x51)))(lt(getItem(x69)(1))(sub(x6)(x52)))))))(randint(3)(7)))(randint(3)(7))))((lambda x70: __dict__(__tuple__(__str__(input))(x65))(__tuple__(__str__(output))(x70)))(canvas(x62)(__tuple__(1)(1)))))))(ifElse(elem(__str__(x56))(dir()))(x56)(None))(ifElse(elem(__str__(x64))(dir()))(x64)(None))(ifElse(elem(__str__(x63))(dir()))(x63)(None))(ifElse(elem(__str__(x57))(dir()))(x57)(None))(ifElse(elem(__str__(x65))(dir()))(x65)(None))(ifElse(elem(__str__(x61))(dir()))(x61)(None))(ifElse(elem(__str__(x40))(dir()))(x40)(None))(ifElse(elem(__str__(x41))(dir()))(x41)(None))(ifElse(elem(__str__(x55))(dir()))(x55)(None))(ifElse(elem(__str__(x51))(dir()))(x51)(None))(ifElse(elem(__str__(x62))(dir()))(x62)(None))(ifElse(elem(__str__(x52))(dir()))(x52)(None))(ifElse(elem(__str__(x58))(dir()))(x58)(None))(ifElse(elem(__str__(x53))(dir()))(x53)(None))(ifElse(elem(__str__(x60))(dir()))(x60)(None))(ifElse(elem(__str__(x68))(dir()))(x68)(None)))(None))(0))(0))(mul(4)(x10)))(asindices(x65)))(unifint(x2)(x3)(__tuple__(1)(9))))(canvas(x7)(__tuple__(x5)(x6))))(remove(x7)(x4)))(choice(x4)))(unifint(x2)(x3)(__tuple__(10)(30))))(unifint(x2)(x3)(__tuple__(10)(30))))(interval(0)(10)(1)))(lambda x71: (lambda x72: x72(x72))(lambda x73: x71(lambda x74: x73(x73)(__star__(x74)))))"

# print(pythonExpr)
print(python_to_stitch(pythonExpr))
# >> (lam (lam (rotf go (choice identity rot90 rot180 rot270) (rotf gi))))
# variables go and gi should be deBruijn indices bound to their respective lambdas
