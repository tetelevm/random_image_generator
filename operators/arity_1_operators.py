"""
Operators with arity 1.

Transform the original value by some mathematical formula. Owns the
0-arity operator, which selects a value for conversion before performing
the conversion.

You can see the `formula` generation using the code:

from from matplotlib import pyplot
x = [a / 1000 for a in range(-1000, 1001)]
y = [formula(a) for a in x]
pyplot.plot(x, y)
pyplot.show()

"""

import math
from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE
from .arity_0_operators import ZERO_OPERATOR


class OneArityOperator(Operator, ABC):
    """
    This is a one-level operator.

    Modifies the original value using the formula from the `formula`
    method.

    Has a `first_sub` that selects the value to use.
    """

    arity = 1
    suboperators: tuple[ZERO_OPERATOR]

    @abstractmethod
    def formula(self, col: float) -> float:
        pass

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
    A function which looks a bit like a well (letter V with rounded
    edges).
    """
    def formula(self, col):
        return 1 - 2 / (1 + col ** 2) ** 8


class Tent(OneArityOperator):
    """
    A function that looks a bit like a tent (two lines (-1;-1)-(0;1) and
    (0;1)-(1;-1)).
    """
    def formula(self, col):
        return 1 - min(abs(col), 1)


class Hyperbole(OneArityOperator):
    """
    A hyperbolic function that changes its value at point 0.
    """
    def formula(self, col):
        return (1 if col >= 0 else -1) * (1 - abs(col) ** 0.5) ** 2


class Circle(OneArityOperator):
    """
    The first and third quarter of the circle.
    """
    def formula(self, col):
        return (1 if col >= 0 else -1) * (1 - min(abs(col), 1) ** 2) ** 0.5


class Arror(OneArityOperator):
    def formula(self, col):
        return 5.8 * col**2 - 6.8 * abs(col) + 1


class Sigmoid(OneArityOperator):
    """
    Standard sigmoid function.
    """
    def formula(self, col):
        return 2 / (1 + math.e ** (-col * 10)) - 1


class Splitter(OneArityOperator):
    """
    Just a line divided into four parts.
    """
    def formula(self, col):
        if col < -0.5:
            return col + 1
        if -0.5 <= col < 0:
            return col - 0.5
        if 0 <= col < 0.5:
            return col + 0.5
        if col >= 0.5:
            return col - 1


class SplitParabola(OneArityOperator):
    """
    It looks like the letter V drawn with a parabola.
    """
    def formula(self, col):
        if col < -0.5:
            return 4 * (max(col, -1) + 0.5)**2
        if -0.5 <= col < 0.5:
            return 4 * col**2 - 1
        if col >= 0.5:
            return 4 * (min(col, 1) - 0.5)**2


class Star(OneArityOperator):
    """
    Four pieces of the four-pointed star.
    """
    def formula(self, col):
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
    Sinus-based color generation function. It has a phase and frequency
    shift.
    """
    def formula(self, col):
        return math.sin(self.phase + self.frequency * col)


class Cos(TrigonometricOperator):
    """
    Cosine-based color generation function. It has a phase and frequency
    shift. Although the phase shift makes this operator similar to a
    sin, but let it be.
    """
    def formula(self, col):
        return math.cos(self.phase + self.frequency * col)


ZERO_ONE_OPERATOR = ZERO_OPERATOR | OneArityOperator

__all__ = operator_subclass_names(locals())
