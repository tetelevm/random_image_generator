"""
Operators with arity equal to 0.

The most basic operators that do not change the value, but only choose
which value the value will be used for the color - x/y/c.
"""

from abc import ABC

from .base import Operator, operator_subclass_names


class ZeroArityOperator(Operator, ABC):
    """
    This is a zero-level operator.
    It does not calculate anything, but only selects which value will be
    used - x/y/c.
    """

    arity = 0

    def func(self, *colors):
        """
        This function is not needed by this class.
        The class does not generate a color, it only selects a value to
        generate, and this function is a stub for the abstractmethod.
        """
        pass


# ======================================================================


class Constant(ZeroArityOperator):
    """
    An operator that does not use position data, but gives only randomly
    generated data.
    """

    def __init__(self):
        super().__init__()
        self.value = (
            self.random.uniform(0, 1),
            self.random.uniform(0, 1),
            self.random.uniform(0, 1),
        )

    def __str_extra_args__(self):
        return [f"value={self.value}"]

    def eval(self, x, y):
        return self.value


class VariableX(ZeroArityOperator):
    """
    An operator that selects only the x-position of a pixel.
    """

    def eval(self, x, y):
        return (x, x, x)


class VariableY(ZeroArityOperator):
    """
    An operator that selects only the y-position of a pixel.
    """

    def eval(self, x, y):
        return (y, y, y)


ZERO_OPERATOR = ZeroArityOperator

__all__ = operator_subclass_names(locals())
