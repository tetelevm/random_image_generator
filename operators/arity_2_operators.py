"""
Operators with arity 2.

Take 2 colors and mix them in some way. Owns two 0/1 arity operators,
which calculate the initial colors.

In this version the values (r, g, b) do not intersect each other and are
calculated separately, but this will change in the future.
"""

from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE
from .arity_1_operators import ZERO_ONE_OPERATOR


class TwoArityOperator(Operator, ABC):
    """
    This is a two-level operator.

    Modifies and mixes the original values using the `func` function.

    Has a `first_col`, `second_col` that generates the original value.
    """

    arity = 2

    @abstractmethod
    def func(self, first_col: COLOR_TYPE, second_col: COLOR_TYPE) -> COLOR_TYPE:
        """
        Color generation function. Accepts data for generation and
        outputs the first color step according to the described formula.
        """
        pass

    def __init__(self, first_sub, second_sub):
        self.first_sub: ZERO_ONE_OPERATOR = first_sub
        self.second_sub: ZERO_ONE_OPERATOR = second_sub

    def eval(self, x, y):
        """
        Generates color with its own suboperators and then passes the
        color calculation to its `func` function.
        """

        first_color = self.first_sub.eval(x, y)
        second_color = self.second_sub.eval(x, y)
        return self.func(first_color, second_color)


# ======================================================================


class Sum(TwoArityOperator):
    """
    Calculates the average between the two colors.
    """

    sort_key = 3

    def func(self, first_col, second_col):
        r = (first_col[0] + second_col[0]) / 2
        g = (first_col[1] + second_col[1]) / 2
        b = (first_col[2] + second_col[2]) / 2
        return (r, g, b)


class Product(TwoArityOperator):
    """
    Multiplies one color by another.
    """

    sort_key = 4

    def func(self, first_col, second_col):
        r = first_col[0] * second_col[0]
        g = first_col[1] * second_col[1]
        b = first_col[2] * second_col[2]
        return (r, g, b)


class Mod(TwoArityOperator):
    """
    Calculates the mod of one color relative to another.
    """

    sort_key = 5

    def func(self, first_col, second_col):
        try:
            r = first_col[0] % second_col[0]
            g = first_col[1] % second_col[1]
            b = first_col[2] % second_col[2]
            return (r, g, b)
        except ZeroDivisionError:
            return (0, 0, 0)


ZERO_ONE_TWO_OPERATOR = ZERO_ONE_OPERATOR | TwoArityOperator

__all__ = operator_subclass_names(locals())
