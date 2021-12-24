from abc import ABC

from .base import Operator, operator_subclass_names


class ThirdArityOperator(Operator, ABC):
    arity = 3

    def __init__(self, first_sub, second_sub, third_sub):
        self.first_sub = first_sub
        self.second_sub = second_sub
        self.third_sub = third_sub


class Level(ThirdArityOperator):
    sort_key = 9

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.treshold = self.random.uniform(-1.0, 1.0)

    def eval(self, x, y):
        (r1, g1, b1) = self.first_sub.eval(x, y)
        (r2, g2, b2) = self.second_sub.eval(x, y)
        (r3, g3, b3) = self.third_sub.eval(x, y)

        r = r2 if r1 < self.treshold else r3
        g = g2 if g1 < self.treshold else g3
        b = b2 if b1 < self.treshold else b3
        return (r, g, b)


class Mix(ThirdArityOperator):
    sort_key = 10

    def eval(self, x, y):
        # In the original script, they apparently forgot to pass `w` as a parameter.
        # w = 0.5 * (self.first_sub.eval(x, y)[0] + 1.0)

        (r1, g1, b1) = self.second_sub.eval(x, y)
        (r2, g2, b2) = self.third_sub.eval(x, y)
        r = (r1 + r2) / 2
        g = (g1 + g2) / 2
        b = (b1 + b2) / 2
        return (r, g, b)


__all__ = operator_subclass_names(locals())
