import math
from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names


class OneArityOperator(Operator, ABC):
    arity = 1

    @abstractmethod
    def func(self, col: float) -> float:
        pass

    def __init__(self, zero_operator):
        self.zero_operator: Operator = zero_operator

    def eval(self, x, y):
        (r, g, b) = self.zero_operator.eval(x, y)
        return (self.func(r), self.func(g), self.func(b))


class TrigonometricOperator(OneArityOperator, ABC):
    def __init__(self, e):
        super().__init__(e)
        self.phase = self.random.uniform(0, math.pi)
        self.freq = self.random.uniform(1.0, 6)


# ======================================================================


class Well(OneArityOperator):
    sort_key = 8

    def func(self, col):
        return 1 - 2 / (1 + col * col) ** 8


class Tent(OneArityOperator):
    sort_key = 7

    def func(self, col):
        return 1 - 2 * abs(col)


# class Phi(OneArityOperator):
#     def func(self, col):
#         return (1 + math.erf(col / math.sqrt(2))) - 1


class Sin(TrigonometricOperator):
    sort_key = 6

    def func(self, col):
        return math.sin(self.phase + self.freq * col)


# class Cos(TrigonometricOperator):
#     def func(self, col):
#         return math.cos(self.phase + self.freq * col)


__all__ = operator_subclass_names(locals())
