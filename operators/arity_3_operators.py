"""
Operators with arity 3.

Take 3 colors and mix them in some way. Own the three 0/1/2 arity
operators, which calculate the original colors. The second and third
colors are mixed, and the third comes as a filter for them.

In this version the values (r, g, b) do not intersect each other and are
calculated separately, but this will change in the future (and is more of
a bug right now).
"""

from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE


class ThirdArityOperator(Operator, ABC):
    arity = 3

    @abstractmethod
    def func(
            self,
            first_col: COLOR_TYPE,
            second_col: COLOR_TYPE,
            third_col: COLOR_TYPE
    ) -> COLOR_TYPE:
        pass

    def __init__(self, first_sub, second_sub, third_sub):
        self.first_sub = first_sub
        self.second_sub = second_sub
        self.third_sub = third_sub

    def eval(self, x, y):
        first_color = self.first_sub.eval(x, y)
        second_color = self.second_sub.eval(x, y)
        third_color = self.third_sub.eval(x, y)
        return self.func(first_color, second_color, third_color)


# ======================================================================


class Level(ThirdArityOperator):
    sort_key = 9

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.treshold = self.random.uniform(-1.0, 1.0)

    def func(self, first_col, second_col, third_col):
        r = second_col[0] if first_col[0] < self.treshold else third_col[0]
        g = second_col[1] if first_col[1] < self.treshold else third_col[1]
        b = second_col[2] if first_col[2] < self.treshold else third_col[2]
        return (r, g, b)


class Mix(ThirdArityOperator):
    sort_key = 10

    def func(self, first_col, second_col, third_col):
        # The original script contains a line:
        # w = 0.5 * (self.first_sub.eval(x, y)[0] + 1.0)
        # But then it does not use the parameter w (most likely a plain bug),
        # so here we do not use the parameter first_col either.

        r = (second_col[0] + third_col[0]) / 2
        g = (second_col[1] + third_col[1]) / 2
        b = (second_col[2] + third_col[2]) / 2
        return (r, g, b)


__all__ = operator_subclass_names(locals())
