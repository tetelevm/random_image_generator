"""
Operators with arity 1.

Transform the original value by some mathematical formula. Owns the
0-arity operator, which selects a value for conversion before performing
the conversion.

In this version the values (r, g, b) do not intersect each other and are
calculated separately, but this will change in the future.
"""

import math
from types import FunctionType, LambdaType
from abc import ABC

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
    suboperators: tuple[ZERO_OPERATOR]

    # it's a method
    formula: FunctionType | LambdaType

    def func(self, col: COLOR_TYPE) -> COLOR_TYPE:
        """
        Color generation function. Accepts data for generation and
        outputs the first color step according to the described formula.
        """
        r = self.formula(col[0])
        g = self.formula(col[1])
        b = self.formula(col[2])
        return (r, g, b)


class TrigonometricOperator(OneArityOperator, ABC):
    """
    Color generation function based on trigonometric operators.
    Has data about the phase and frequency of the operation.
    """

    def __self_init__(self):
        self.phase: float = self.random.uniform(0, math.pi)
        self.frequency: float = self.random.uniform(1.0, 6)

    def __str_extra_args__(self):
        return [f"phase={self.phase}", f"frequency={self.frequency}"]


# ======================================================================


class Well(OneArityOperator):
    """
    A function which looks a bit like a well.
    (description from the original script)
    """
    formula = lambda s, col: 1 - 2 / (1 + col ** 2) ** 8


class Tent(OneArityOperator):
    """
    A function that looks a bit like a tent.
    (description from the original script)
    """
    formula = lambda s, col: 1 - 2 * abs(col)


class Hyperbole(OneArityOperator):
    formula = lambda s, col: (1 if col >= 0 else -1) * (1 - abs(col) ** 0.5) ** 2


class Circle(OneArityOperator):
    formula = lambda s, col: (1 if col >= 0 else -1) * (1 - col ** 2) ** 0.5


class Arror(OneArityOperator):
    formula = lambda s, col: 5.8 * col**2 - 6.8 * abs(col) + 1


class Splitter(OneArityOperator):
    def formula(self, col: float) -> float:
        if col < -0.5:
            return col + 1
        if -0.5 <= col < 0:
            return col - 0.5
        if 0 <= col < 0.5:
            return col + 0.5
        if col >= 0.5:
            return col - 1


class SplitParabola(OneArityOperator):
    def formula(self, col: float) -> float:
        if col < -0.5:
            return 4 * (col + 0.5)**2
        if -0.5 <= col < 0.5:
            return 4 * col**2 - 1
        if col >= 0.5:
            return 4 * (col - 0.5)**2


class Star(OneArityOperator):
    def formula(self, col: float) -> float:
        third = 1/3
        if col < -third:
            return 0.5 * (col + 1)
        if -third <= col < 0:
            return -2 * col - 1
        if 0 <= col < third:
            return -2 * col + 1
        if col >= third:
            return 0.5 * (col - 1)


class Sin(TrigonometricOperator):
    """
    Sinus-based color generation function.
    """
    formula = lambda s, col: math.sin(s.phase + s.frequency * col)


class Cos(TrigonometricOperator):
    """
    Cosinus-based color generation function.
    """
    formula = lambda s, col: math.cos(s.phase + s.frequency * col)


ZERO_ONE_OPERATOR = ZERO_OPERATOR | OneArityOperator

__all__ = operator_subclass_names(locals())
