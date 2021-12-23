from abc import ABC

from .base import Operator, operator_subclass_names


class ThirdArityOperator(Operator, ABC):
    arity = 3


class Level(ThirdArityOperator):
    sort_key = 9

    def __init__(self, level, e1, e2):
        self.treshold = self.random.uniform(-1.0, 1.0)
        self.level = level
        self.e1 = e1
        self.e2 = e2

    def eval(self, x, y):
        (r1, g1, b1) = self.level.eval(x, y)
        (r2, g2, b2) = self.e1.eval(x, y)
        (r3, g3, b3) = self.e2.eval(x, y)
        r4 = r2 if r1 < self.treshold else r3
        g4 = g2 if g1 < self.treshold else g3
        b4 = b2 if b1 < self.treshold else b3
        return (r4, g4, b4)


class Mix(ThirdArityOperator):
    sort_key = 10

    def __init__(self, w, e1, e2):
        self.w = w
        self.e1 = e1
        self.e2 = e2

    def eval(self, x, y):
        # In the original script, they apparently forgot to pass `w` as a parameter.
        # w = 0.5 * (self.w.eval(x, y)[0] + 1.0)

        (r1, g1, b1) = self.e1.eval(x, y)
        (r2, g2, b2) = self.e2.eval(x, y)
        r3 = (r1 + r2) / 2
        g3 = (g1 + g2) / 2
        b3 = (b1 + b2) / 2
        return (r3, g3, b3)


__all__ = operator_subclass_names(locals())
