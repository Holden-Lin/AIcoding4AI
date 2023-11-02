import argparse
import fire


class Calculator(object):
    """A simple calculator class."""

    def double(self, number):
        return 2 * number

    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

    def minus(self, a, b):
        return a - b


# Function to parse command-line arguments
"""
1. help parameter is used to display the help messages for each argument like below:

$ python script.py -h
...
  action        add/minus/multiply/double
  x             the first number
  y             the second number
...

2. The nargs parameter specifies how many command-line arguments should be consumed.

The ? character indicates that the argument is optional and if not provided, the default value will be used.
Other possible values for nargs:
- a constant number
- * : Specifies that any number of arguments (including none) should be consumed and stored in a list.
- + : Specifies that at least one argument should be consumed, with all arguments stored in a list.

"""


def parser_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("action", help="add/minus/multiply/double")
    parser.add_argument("x", type=int, help="the first number")
    parser.add_argument("y", nargs="?", type=int, help="the second number", default=0)
    args = parser.parse_args()

    return args


# Function to perform the specified action using the parsed arguments


def action(args):
    ctl = Calculator()
    action = args.action

    numbers = [args.x, args.y] if action != "double" else [args.x]

    # getattr is a built-in function in Python that allows you to access the attribute of an object by name (as a string).
    # getattr(ctl, action) is attempting to fetch the method of the Calculator object ctl \
    # whose name matches the string contained in the variable action.
    # The * operator is used for argument unpacking. It unpacks the elements of numbers (which is a list) \
    # into positional arguments.  eg. if numbers is [5, 3], then *numbers unpacks this list into two separate arguments, \
    # effectively becoming 5, 3.
    res = getattr(ctl, action)(*numbers)
    print(res)


def main():
    args = parser_args()
    action(args=args)


if __name__ == "__main__":
    main()

"""
python argparse_demo.py add 1 2
# 调用add方法，将1和2相加，输出结果3
python argparse_demo.py multiply 2 3
# 调用multiply方法，将2和3相乘，输出结果6
python argparse_demo.py minus 2 3
# 调用minus方法，从2中减去3，输出结果-1
"""
