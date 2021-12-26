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


class OneArityOperator(Operator, ABC):
    arity = 1

    @abstractmethod
    def func(self, col: COLOR_TYPE) -> COLOR_TYPE:
        pass

    def __init__(self, zero_operator):
        self.zero_operator: Operator = zero_operator

    def eval(self, x, y):
        color = self.zero_operator.eval(x, y)
        return self.func(color)


class TrigonometricOperator(OneArityOperator, ABC):
    def __init__(self, zero_operator):
        super().__init__(zero_operator)
        self.phase = self.random.uniform(0, math.pi)
        self.freq = self.random.uniform(1.0, 6)


# ======================================================================


class Well(OneArityOperator):
    sort_key = 8

    def func(self, col):
        r = 1 - 2 / (1 + col[0] ** 2) ** 8
        g = 1 - 2 / (1 + col[1] ** 2) ** 8
        b = 1 - 2 / (1 + col[2] ** 2) ** 8
        return (r, g, b)


class Tent(OneArityOperator):
    sort_key = 7

    def func(self, col):
        r = 1 - 2 * abs(col[0])
        g = 1 - 2 * abs(col[1])
        b = 1 - 2 * abs(col[2])
        return (r, g, b)


class Sin(TrigonometricOperator):
    sort_key = 6

    def func(self, col):
        r = math.sin(self.phase + self.freq * col[0])
        g = math.sin(self.phase + self.freq * col[1])
        b = math.sin(self.phase + self.freq * col[2])
        return (r, g, b)


__all__ = operator_subclass_names(locals())
