"""
Operators with arity 2.

Take 2 colors and mix them in some way. Owns two 0/1 arity operators,
which calculate the initial colors.

In this version the values (r, g, b) do not intersect each other and are
calculated separately, but this will change in the future.
"""

from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE


class SecondArityOperator(Operator, ABC):
    arity = 2

    @abstractmethod
    def func(self, first_col: COLOR_TYPE, second_col: COLOR_TYPE) -> COLOR_TYPE:
        pass

    def __init__(self, first_sub, second_sub):
        self.first_sub: Operator = first_sub
        self.second_sub: Operator = second_sub

    def eval(self, x, y):
        first_color = self.first_sub.eval(x, y)
        second_color = self.second_sub.eval(x, y)
        return self.func(first_color, second_color)


# ======================================================================


class Sum(SecondArityOperator):
    sort_key = 3

    def func(self, first_col, second_col):
        r = (first_col[0] + second_col[0]) / 2
        g = (first_col[1] + second_col[1]) / 2
        b = (first_col[2] + second_col[2]) / 2
        return (r, g, b)


class Product(SecondArityOperator):
    sort_key = 4

    def func(self, first_col, second_col):
        r = first_col[0] * second_col[0]
        g = first_col[1] * second_col[1]
        b = first_col[2] * second_col[2]
        return (r, g, b)


class Mod(SecondArityOperator):
    sort_key = 5

    def func(self, first_col, second_col):
        try:
            r = first_col[0] % second_col[0]
            g = first_col[1] % second_col[1]
            b = first_col[2] % second_col[2]
            return (r, g, b)
        except ZeroDivisionError:
            return (0, 0, 0)


__all__ = operator_subclass_names(locals())
