"""
    Contains the standard re-arc utils with some additions:
        - functions with two or more arguments have been curried,
        - operator functions like `sub` and `add` have been added,
        - a plotting function is included for visualizations.
"""

import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize

# Custom curried random functions
from curried_random import choice, randint, sample, shuffle, uniform

from dsl import *


global rng
rng = []

def curry(func):
    def curried(*args):
        if len(args) == func.__code__.co_argcount:
            return func(*args)
        else:
            return lambda x: curried(*(args + (x,)))
    return curried


@curry
def sub(
    a: float,
    b: float
) -> float:
    """
    returns a - b
    """
    return a - b

@curry
def add(
    a: float,
    b: float
) -> float:
    """
    returns a + b
    """
    return a + b

@curry
def div(
    a: float,
    b: float
) -> float:
    """
    returns a/b
    """
    return a/b

@curry
def floordiv(
        a: float,
        b: float,
) -> int:
    """
    returns a//b
    """
    return a // b

@curry
def eq(
    a: Any,
    b: Any
) -> bool:
    """
    returns True iff a is equal to b
    """
    return a == b

@curry
def neq(
    a: Any,
    b: Any
) -> bool:
    """
    returns True iff a is not equal to b
    """
    return a != b

@curry
def gt(
    a: Any,
    b: Any
) -> bool:
    """
    returns True if a is greater than b
    """
    return a > b

@curry
def gte(
    a: Any,
    b: Any
) -> bool:
    """
    returns True if a is greater than or equal to b
    """
    return a >= b

@curry
def lt(
    a: Any,
    b: Any
) -> bool:
    """
    returns True if a is less than b
    """
    return a < b

@curry
def lte(
    a: Any,
    b: Any
) -> bool:
    """
    returns True if a is less than or equal to b
    """
    return a <= b

@curry
def unifint(
    diff_lb: float,
    diff_ub: float,
    bounds: Tuple[int, int]
) -> int:
    """
    diff_lb: lower bound for difficulty, must be in range [0, diff_ub]
    diff_ub: upper bound for difficulty, must be in range [diff_lb, 1]
    bounds: interval [a, b] determining the integer values that can be sampled
    """
    a, b = bounds
    d = uniform(diff_lb, diff_ub)
    global rng
    rng.append(d)
    return min(max(a, round(a + (b - a) * d)), b)

@curry
def is_grid(
    grid: Any
) -> bool:
    """
    returns True if and only if argument is a valid grid
    """
    if not isinstance(grid, tuple):
        return False
    if not 0 < len(grid) <= 30:
        return False
    if not all(isinstance(r, tuple) for r in grid):
        return False
    if not all(0 < len(r) <= 30 for r in grid):
        return False
    if not len(set(len(r) for r in grid)) == 1:
        return False
    if not all(all(isinstance(x, int) for x in r) for r in grid):
        return False
    if not all(all(0 <= x <= 9 for x in r) for r in grid):
        return False
    return True

@curry
def strip_prefix(
    string: str,
    prefix: str
) -> str:
    """
    removes prefix
    """
    return string[len(prefix):]

@curry
def format_grid(
    grid: List[List[int]]
) -> Grid:
    """
    grid type casting
    """
    return tuple(tuple(row) for row in grid)

@curry
def format_example(
    example: dict
) -> dict:
    """
    example data type
    """
    return {
        'input': format_grid(example['input']),
        'output': format_grid(example['output'])
    }

@curry
def format_task(
    task: dict
) -> dict:
    """
    task data type
    """
    return {
        'train': [format_example(example) for example in task['train']],
        'test': [format_example(example) for example in task['test']]
    }

@curry
def plot_task(
    task: List[dict],
    title: str = None
) -> None:
    """
    displays a task with two dictionaries:
    first dictionary on top row, second dictionary on bottom row
    
    Args:
        task: List containing exactly two dictionaries with 'input' and 'output' keys
        title: Optional title for the plot
    """
    if len(task) != 2:
        raise ValueError("Task must contain exactly 2 dictionaries")
        
    cmap = ListedColormap([
        '#000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00',
        '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25'
    ])
    norm = Normalize(vmin=0, vmax=9)
    args = {'cmap': cmap, 'norm': norm}
    
    # Create a 2x1 subplot (2 rows, 1 column)
    figure, axes = plt.subplots(2, 2, figsize=(6, 6))
    
    # Plot first dictionary on top row
    axes[0, 0].imshow(task[0]['input'], **args)
    axes[0, 1].imshow(task[0]['output'], **args)
    
    # Plot second dictionary on bottom row
    axes[1, 0].imshow(task[1]['input'], **args)
    axes[1, 1].imshow(task[1]['output'], **args)
    
    # Hide ticks for all axes
    for row in axes:
        for ax in row:
            ax.set_xticks([])
            ax.set_yticks([])
    
    if title is not None:
        figure.suptitle(title, fontsize=20)

    plt.subplots_adjust(wspace=0.1, hspace=0.1)
    print(os.getcwd())
    plt.savefig(os.path.join(".", "reArc", "test_figures", "testingLambdas.png"))


@curry
def fix_bugs(
    dataset: dict
) -> None:
    """
    fixes bugs in the original ARC training dataset
    """
    dataset['a8d7556c']['train'][2]['output'] = fill(dataset['a8d7556c']['train'][2]['output'], 2, {(8, 12), (9, 12)})
    dataset['6cf79266']['train'][2]['output'] = fill(dataset['6cf79266']['train'][2]['output'], 1, {(6, 17), (7, 17), (8, 15), (8, 16), (8, 17)})
    dataset['469497ad']['train'][1]['output'] = fill(dataset['469497ad']['train'][1]['output'], 7, {(5, 12), (5, 13), (5, 14)})
    dataset['9edfc990']['train'][1]['output'] = fill(dataset['9edfc990']['train'][1]['output'], 1, {(6, 13)})
    dataset['e5062a87']['train'][1]['output'] = fill(dataset['e5062a87']['train'][1]['output'], 2, {(1, 3), (1, 4), (1, 5), (1, 6)})
    dataset['e5062a87']['train'][0]['output'] = fill(dataset['e5062a87']['train'][0]['output'], 2, {(5, 2), (6, 3), (3, 6), (4, 7)})
