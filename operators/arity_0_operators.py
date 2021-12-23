from abc import ABC
# from itertools import product

from .base import Operator, operator_subclass_names


class ZeroArityOperator(Operator, ABC):
    arity = 0


# class PositionOperator(ZeroArityOperator, ABC):
#     r: str
#     g: str
#     b: str
#
#     def eval(self, x, y):
#         kwargs = {"x": x, "y": y}
#         return (kwargs[self.r], kwargs[self.g], kwargs[self.b])


# ======================================================================


class Constant(ZeroArityOperator):
    sort_key = 2

    def __init__(self):
        self.value = (
            self.random.uniform(0, 1),
            self.random.uniform(0, 1),
            self.random.uniform(0, 1),
        )

    def eval(self, x, y):
        return self.value


class VariableX(ZeroArityOperator):
    sort_key = 0

    def eval(self, x, y):
        return (x, x, x)


class VariableY(ZeroArityOperator):
    sort_key = 1

    def eval(self, x, y):
        return (y, y, y)


# # VariableXXX - VariableYYY
# for (r, g, b) in product("xy", repeat=3):
#     name = "Variable" + (r+g+b).upper()
#     _class = type(
#         name,
#         (PositionOperator,),
#         {"r": r, "g": g, "b": b}
#     )
#     locals()[name] = _class


__all__ = operator_subclass_names(locals())
