"""
Operators with arity equal to 0.

The most basic operators that do not change the value, but only choose
which value the value will be used for the color - x/y/c.
"""

from abc import ABC
from itertools import product

from .base import OperatorManager, Operator, operator_subclass_names


class ZeroArityOperator(Operator, ABC):
    """
    This is a zero-level operator.
    It does not calculate anything, but only selects which value will be
    used - x/y/c.
    """

    arity = 0
    xyc_index: list[int]

    def __self_init__(self):
        self.value = self.random.uniform(-1, 1)

    def __str_extra_args__(self):
        return [f"value={self.value}"]

    def eval(self, x, y):
        xyc_cols = [x, y, self.value]
        return (
            xyc_cols[self.xyc_index[0]],
            xyc_cols[self.xyc_index[1]],
            xyc_cols[self.xyc_index[2]],
        )

    def func(self, *colors):
        """
        This function is not needed by this class.
        The class does not generate a color, it only selects a value to
        generate, and this function is a stub for the abstractmethod.
        """
        pass


# ======================================================================


# VariableXXX, VariableXXY, VariableXXC, ..., VariableXYX, ..., VariableCCC
for (r, g, b) in product("xyc", repeat=3):
    class_name = "Variable" + r.upper() + g.upper() + b.upper()
    indexes = ["xyc".find(r), "xyc".find(g), "xyc".find(b)]
    doc = f"An operator that selects only the {r}{g}{b}-position of a pixel."
    locals()[class_name] = OperatorManager(
        class_name,
        (ZeroArityOperator,),
        {"xyc_index": indexes, "__doc__": doc}
    )


ZERO_OPERATOR = ZeroArityOperator

__all__ = operator_subclass_names(locals())
