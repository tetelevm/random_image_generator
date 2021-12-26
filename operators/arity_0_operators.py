"""
Operators with arity equal to 0.

The most basic operators that do not change the value, but only choose
which value the value will be used for the color - x/y/c.
"""

from abc import ABC

from .base import Operator, operator_subclass_names


class ZeroArityOperator(Operator, ABC):
    arity = 0


# ======================================================================


class Constant(ZeroArityOperator):
    sort_key = 2

    def __init__(self):
        self.value = (
            self.random.uniform(0, 1),
            self.random.uniform(0, 1),
            self.random.uniform(0, 1),
        )

    def eval(self, x, y):
        return self.value


class VariableX(ZeroArityOperator):
    sort_key = 0

    def eval(self, x, y):
        return (x, x, x)


class VariableY(ZeroArityOperator):
    sort_key = 1

    def eval(self, x, y):
        return (y, y, y)


__all__ = operator_subclass_names(locals())
