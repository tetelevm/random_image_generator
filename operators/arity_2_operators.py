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
        (r1, g1, b1) = first_col
        (r2, g2, b2) = second_col
        r3 = (r1 + r2) / 2
        g3 = (g1 + g2) / 2
        b3 = (b1 + b2) / 2
        return (r3, g3, b3)


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
        except:
            return (0, 0, 0)


__all__ = operator_subclass_names(locals())
