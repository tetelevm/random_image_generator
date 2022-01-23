"""
Operators with arity 1.

Transform the original value by some mathematical formula. Owns the
0-arity operator, which selects a value for conversion before performing
the conversion.

In this version the values (r, g, b) do not intersect each other and are
calculated separately, but this will change in the future.
"""

import math
from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE
from .arity_0_operators import ZERO_OPERATOR


class OneArityOperator(Operator, ABC):
    """
    This is a one-level operator.

    Changes the original value using the mathematical formula described
    in the `func` function.

    Has a `first_sub` that selects the value to use.
    """

    arity = 1

    @abstractmethod
    def func(self, col: COLOR_TYPE) -> COLOR_TYPE:
        """
        Color generation function. Accepts data for generation and
        outputs the first color step according to the described formula.
        """
        pass

    def __init__(self, first_sub):
        self.first_sub: ZERO_OPERATOR = first_sub

    def eval(self, x, y):
        """
        Generates color with its own suboperators and then passes the
        color calculation to its `func` function.
        """

        color = self.first_sub.eval(x, y)
        return self.func(color)


class TrigonometricOperator(OneArityOperator, ABC):
    """
    Color generation function based on trigonometric operators.
    Has data about the phase and frequency of the operation.
    """

    def __init__(self, zero_operator):
        super().__init__(zero_operator)
        self.phase: float = self.random.uniform(0, math.pi)
        self.frequency: float = self.random.uniform(1.0, 6)


# ======================================================================


class Well(OneArityOperator):
    """
    A function which looks a bit like a well.
    (description from the original script)
    """

    def func(self, col):
        r = 1 - 2 / (1 + col[0] ** 2) ** 8
        g = 1 - 2 / (1 + col[1] ** 2) ** 8
        b = 1 - 2 / (1 + col[2] ** 2) ** 8
        return (r, g, b)


class Tent(OneArityOperator):
    """
    A function that looks a bit like a tent.
    (description from the original script)
    """

    def func(self, col):
        r = 1 - 2 * abs(col[0])
        g = 1 - 2 * abs(col[1])
        b = 1 - 2 * abs(col[2])
        return (r, g, b)


class Sin(TrigonometricOperator):
    """
    Sinus-based color generation function.
    """

    def func(self, col):
        r = math.sin(self.phase + self.frequency * col[0])
        g = math.sin(self.phase + self.frequency * col[1])
        b = math.sin(self.phase + self.frequency * col[2])
        return (r, g, b)


ZERO_ONE_OPERATOR = ZERO_OPERATOR | OneArityOperator

__all__ = operator_subclass_names(locals())
