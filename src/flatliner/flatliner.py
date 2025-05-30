import ast

def construct_lambda(vals: dict[str, str], body: str = '{}') -> str:
    """
    Returns a lambda function string with the arguments provided.
    >>> construct_lambda({'a': '1', 'b': '2'})
    '(lambda a, b: {})(1, 2)'
    >>> exec(construct_lambda({'a': '1', 'b': '2'}, 'print(a + b)'))
    3
    """
    return f'(lambda {", ".join(vals.keys())}: {body})({", ".join(vals.values())})'


def provide_y(body: str) -> str:
    """
    provides the Y combinator.
    """
    return construct_lambda({'_Y': '(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args))))'}, body)


def wrap_globals(body: str):
    """
    Wraps a lambda body with the globals dict.
    >>> wrap_globals('print(a)')
    '(lambda __g: print(a))(globals())'
    """
    return construct_lambda({'__g': 'globals()'}, body)


class Flatliner:
    def __init__(self):
        self.ast = None
        self.needs_y = False
        self.loop_no = 1
        self.node_handlers = {
            ast.Assign: self.handle_assign,
            ast.AugAssign: self.handle_augassign,
            ast.Constant: self.handle_constant,
            ast.Expr: self.handle_expr,
            ast.keyword: self.handle_keyword,
            ast.Call: self.handle_call,
            ast.Name: self.handle_name,
            ast.Raise: self.handle_raise,
            ast.Assert: self.handle_assert,
            ast.Pass: self.handle_pass,
            ast.Break: self.handle_loop_flow,
            ast.Continue: self.handle_loop_flow,
            ast.While: self.handle_while,
            ast.For: self.handle_for,
            ast.List: self.handle_list,
            ast.Tuple: self.handle_tuple,
            ast.Set: self.handle_set,
            ast.Dict: self.handle_dict,
            ast.Subscript: self.handle_subscript,
            ast.Slice: self.handle_slice,
            ast.Attribute: self.handle_attribute,
            ast.BinOp: self.handle_binop,
            ast.If: self.handle_if,
            ast.IfExp: self.handle_if,
            list: self.unparse_list,
            ast.Compare: self.handle_compare,
            ast.BoolOp: self.handle_boolop,
            ast.UnaryOp: self.handle_unaryop,
            ast.FunctionDef: self.handle_functiondef,
            ast.ClassDef: self.handle_classdef,
            ast.Return: self.handle_return,
            ast.Import: self.handle_import,
            ast.ImportFrom: self.handle_importfrom,
        }

    def set_ast(self, infile: str):
        """
        Turns the infile into an AST and sets the instance attribute accordingly.
        """
        file = open(infile, 'r')
        self.ast = ast.parse(file.read())
        file.close()

    def apply_handler(self, node, cont=None):
        return self.node_handlers.get(type(node), self.handle_error)(node, cont)

    def handle_constant(self, node, cont) -> str:
        return repr(node.value)

    def handle_name(self, node, cont) -> str:
        return node.id

    def handle_pass(self, node, cont) -> str:
        return cont

    def handle_loop_flow(self, node, cont) -> str:
        return node.contents

    def handle_raise(self, node, cont) -> str:
        return f'(_ for _ in []).throw({self.apply_handler(node.exc)})'

    def handle_assert(self, node, cont) -> str:
        message = '' if node.msg is None else f'({self.apply_handler(node.msg)})'
        error = ast.parse(f'raise AssertionError{message}').body[0]
        return f'({cont} if {self.apply_handler(node.test)} else {self.apply_handler(error)})'

    def _next_item(self) -> str:
        return f'next(_items{self.loop_no}, _term{self.loop_no})'

    def handle_while(self, node, cont) -> str:
        self.needs_y = True
        assigned_in_loop = {self.apply_handler(n.targets[0]) for n in ast.walk(node) if isinstance(n, ast.Assign)
                            and not isinstance(n.targets[0], (ast.Attribute, ast.Subscript, ast.Tuple))
                            and len(n.targets) == 1}
        assigned_in_loop |= {self.apply_handler(n.target) for n in ast.walk(node) if isinstance(n, ast.AugAssign)
                             and not isinstance(n.target, (ast.Attribute, ast.Subscript))}
        assigned_in_loop |= {self.apply_handler(child) for n in ast.walk(node) if isinstance(n, ast.Assign)
                             and isinstance(n.targets[0], ast.Tuple) for child in n.targets[0].elts if
                             not any(isinstance(n2, (ast.Attribute, ast.Subscript)) for n2 in ast.walk(child))}
        assigned_in_loop = sorted(assigned_in_loop)
        args = ', '.join(assigned_in_loop)
        loop_test = self.apply_handler(node.test)
        loop_id = f'_loop{self.loop_no}'
        loop_call = f'{loop_id}({args})'
        for n in ast.walk(node):
            if isinstance(n, ast.Break):
                n.contents = cont
            if isinstance(n, ast.Continue):
                if hasattr(node, 'target'):
                    n.contents = construct_lambda({node.target: self._next_item()}, loop_call)
                else:
                    n.contents = loop_call
        self.loop_no += 1
        loop_body = self.apply_handler(node.body, loop_call)
        loop_repr = construct_lambda(
            {loop_id: f'_Y(lambda {loop_id}: (lambda {args}: ({loop_body}) if {loop_test} else {cont}))'}, loop_call)
        return construct_lambda({v: f'{v} if "{v}" in dir() else None' for v in assigned_in_loop}, loop_repr)

    def handle_for(self, node, cont) -> str:
        target_id = f'_targ{self.loop_no}'
        iter_id = f'_items{self.loop_no}'
        term_id = f'_term{self.loop_no}'
        pre = ast.parse(f'{self.apply_handler(node.target)} = {target_id}').body
        post = ast.parse(f'{target_id} = {self._next_item()}').body
        body_list = pre + node.body + post
        while_test = ast.parse(f'{target_id} is not {term_id}').body[0]
        while_equivalent = ast.While(while_test, body_list)
        while_equivalent.target = target_id
        return construct_lambda({term_id: '[]', iter_id: f'iter({self.apply_handler(node.iter)})'},
                                construct_lambda({target_id: self._next_item()},
                                                 self.apply_handler(while_equivalent, cont)))

    def _handle_container(self, node) -> str:
        return ', '.join(self.apply_handler(child) for child in node.elts)

    def handle_list(self, node, cont) -> str:
        return f'[{self._handle_container(node)}]'

    def handle_tuple(self, node, cont) -> str:
        return f'({self._handle_container(node)}{"," * (len(node.elts) == 1)})'

    def handle_set(self, node, cont) -> str:
        return '{' + self._handle_container(node) + '}'

    def handle_dict(self, node, cont) -> str:
        return '{' + ', '.join(f'{k}: {v}' for k, v in zip(map(self.apply_handler, node.keys),
                                                           map(self.apply_handler, node.values))) + '}'

    def handle_slice(self, node, cont) -> str:
        parts = [self.apply_handler(n) if n is not None else '' for n in [node.lower, node.upper, node.step]]
        return ':'.join(parts)

    def handle_subscript(self, node, cont) -> str:
        print('activated')
        if isinstance(node.slice, ast.Tuple):
            return f'{self.apply_handler(node.value)}[{self.apply_handler(node.slice)[1:-1]}]'
        return f'{self.apply_handler(node.value)}[{self.apply_handler(node.slice)}]'

    def handle_attribute(self, node, cont) -> str:
        return f'{self.apply_handler(node.value)}.{node.attr}'

    def handle_assign(self, node, cont) -> str:
        if len(node.targets) > 1:
            targets = [self.apply_handler(t) for t in node.targets]
            return f'[{cont} for {", ".join(targets)} in [[{self.apply_handler(node.value)}] * {len(targets)}]][0]'
        target = node.targets[0]
        if isinstance(target, (ast.Attribute, ast.Subscript, ast.Tuple, ast.List)):
            return f'[{cont} for {self.apply_handler(target)} in [{self.apply_handler(node.value)}]][0]'
        return construct_lambda({self.apply_handler(target): self.apply_handler(node.value)}, cont)

    def handle_augassign(self, node, cont) -> str:
        assign_equivalent = ast.Assign([node.target], ast.BinOp(node.target, node.op, node.value))
        return self.apply_handler(assign_equivalent, cont)

    def handle_expr(self, node, cont) -> str:
        return self.apply_handler(node.value, cont)

    def handle_keyword(self, node, cont) -> str:
        return f'{node.arg}={self.apply_handler(node.value)}'

    def handle_call(self, node, cont) -> str:
        args = ', '.join(self.apply_handler(child) for child in node.args + node.keywords)
        call = f'{self.apply_handler(node.func)}({args})'
        return call if not cont else f'[{call}, {cont}][-1]'

    def handle_binop(self, node, cont) -> str:
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.FloorDiv: '//',
            ast.Mod: '%',
            ast.Pow: '**',
            ast.LShift: '<<',
            ast.RShift: '>>',
            ast.BitOr: '|',
            ast.BitXor: '^',
            ast.BitAnd: '&',
        }
        return f'({self.apply_handler(node.left)} {op_map[type(node.op)]} {self.apply_handler(node.right)})'

    def handle_boolop(self, node, cont) -> str:
        op_map = {
            ast.And: 'and',
            ast.Or: 'or',
        }
        return f' {op_map[type(node.op)]} '.join(self.apply_handler(child) for child in node.values)

    def handle_unaryop(self, node, cont) -> str:
        op_map = {
            ast.UAdd: '+',
            ast.USub: '-',
            ast.Not: 'not ',
            ast.Invert: '~',
        }
        if isinstance(node.operand, (ast.Name, ast.Constant)):
            return f'{op_map[type(node.op)]}{self.apply_handler(node.operand)}'
        return f'{op_map[type(node.op)]}({self.apply_handler(node.operand)})'

    def handle_if(self, node, cont) -> str:
        return f'({self.apply_handler(node.body, cont)} if {self.apply_handler(node.test)} else {self.apply_handler(node.orelse, cont)})'

    def handle_compare(self, node, cont) -> str:
        op_map = {
            ast.Gt: '>',
            ast.Lt: '<',
            ast.GtE: '>=',
            ast.LtE: '<=',
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.In: 'in',
            ast.Is: 'is',
            ast.IsNot: 'is not',
            ast.NotIn: 'not in',
        }
        comparisons = ''.join(f' {op_map[type(op)]} ' + self.apply_handler(val)
                              for op, val in zip(node.ops, node.comparators))
        return f'({self.apply_handler(node.left)}{comparisons})'

    # def handle_methoddef(self, node, cont) -> str:
    #     all_args = [arg.arg for arg in node.args.args]
    #     defaults = [f'={self.apply_handler(val)}' for val in node.args.defaults]
    #     padding = [''] * (len(all_args) - len(defaults))
    #     args = ', '.join(arg + val for arg, val in zip(all_args, padding + defaults))
    #     for n in ast.walk(node):
    #         if cont and isinstance(n, ast.Call) and self.apply_handler(n.func) == cont.split('.')[0]:
    #             n.func.id = 'self.__class__'
    #     if cont.endswith('__init__'):
    #         return f'lambda{" " if args else ""}{args}: [{self.apply_handler(node.body)}, None][-1]'
    #     if any(isinstance(n, ast.Call) and self.apply_handler(n.func) == node.name for n in ast.walk(node)):
    #         self.needs_y = True
    #         return f'_Y(lambda {node.name}: (lambda {args}: {self.apply_handler(node.body)}))'
    #     return f'lambda{" " if args else ""}{args}: {self.apply_handler(node.body)}'
    
    def handle_methoddef(self, node, cont) -> str:
        # Extract all argument names
        all_args = [arg.arg for arg in node.args.args]
        
        # Handle defaults
        defaults = [f'={self.apply_handler(val)}' for val in node.args.defaults]
        padding = [''] * (len(all_args) - len(defaults))
        
        # Create argument string - ensure no tuples in parameter position
        args_str = ", ".join(all_args)  # Join as individual parameters
        
        # Add default values correctly 
        if defaults:
            args_with_defaults = []
            for i, arg in enumerate(all_args):
                if i >= len(all_args) - len(defaults):
                    default_idx = i - (len(all_args) - len(defaults))
                    args_with_defaults.append(f"{arg}{defaults[default_idx]}")
                else:
                    args_with_defaults.append(arg)
            args_str = ", ".join(args_with_defaults)
        
        # Handle recursive function calls
        for n in ast.walk(node):
            if cont and isinstance(n, ast.Call) and self.apply_handler(n.func) == cont.split('.')[0]:
                n.func.id = 'self.__class__'
                
        # Create appropriate lambda
        if cont.endswith('__init__'):
            return f'lambda{" " if args_str else ""}{args_str}: [{self.apply_handler(node.body)}, None][-1]'
        if any(isinstance(n, ast.Call) and self.apply_handler(n.func) == node.name for n in ast.walk(node)):
            self.needs_y = True
            return f'_Y(lambda {node.name}: (lambda {args_str}: {self.apply_handler(node.body)}))'
        return f'lambda{" " if args_str else ""}{args_str}: {self.apply_handler(node.body)}'

    def handle_functiondef(self, node, cont) -> str:
        curr = self.handle_methoddef(node, '')
        for n in node.decorator_list[::-1]:
            curr = f"{self.apply_handler(n)}({curr})"
        # return construct_lambda({node.name: curr}, cont) # Removed this to avoid wrapping expression in lambda: None
        return curr

    def handle_classdef(self, node, cont) -> str:
        attr_dict = {}
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                attr_dict[n.name] = self.handle_methoddef(n, f'{node.name}.{n.name}')
        bases = ''.join(self.apply_handler(n) + ', ' for n in node.bases)
        attr_repr = '{' + ', '.join(f'{repr(k)}: {v}' for k, v in attr_dict.items()) + '}'
        return construct_lambda({node.name: f'type("{node.name}", ({bases}), {attr_repr})'}, cont)

    def handle_return(self, node, cont) -> str:
        if node.value is None:
            return 'None'
        return self.apply_handler(node.value)

    def handle_import(self, node, cont) -> str:
        imports = [(a.asname if a.asname else a.name, a.name) for a in node.names]
        return construct_lambda({name.split('.')[0]: f"__import__('{mod}')" for name, mod in imports}, cont)

    def handle_importfrom(self, node, cont) -> str:
        imports = [(a.asname if a.asname else a.name, a.name) for a in node.names]
        return construct_lambda({'_mod': f"__import__('{node.module}', {{}}, {{}}, {[i[1] for i in imports]})"},
                                construct_lambda({name: f'_mod.{submodule}' for name, submodule in imports}, cont))

    def handle_error(self, node, cont) -> str:
        return ast.unparse(node)

    def unparse_list(self, body: list, cont=None) -> str:
        temp = cont
        for node in body[::-1]:
            if not isinstance(node, ast.Expr) or isinstance(node.value, ast.Call):
                temp = self.apply_handler(node, temp)
        return str(temp)

    def unparse(self) -> str:
        """
        Unparses the ast.
        """
        self.needs_y = False
        self.loop_no = 1
        curr = self.ast
        if hasattr(curr, 'body') and isinstance(curr.body, list):
            body = self.apply_handler(curr.body)
            return provide_y(body) if self.needs_y else body
        return 'Unparse unsuccessful.'
