"""
Operators with arity 2.

Take 2 colors and mix them in some way. Owns two 0/1 arity operators,
which calculate the initial colors.

In this version the values (r, g, b) do not intersect each other and are
calculated separately, but this will change in the future.
"""

from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE
from .arity_1_operators import ZERO_ONE_OPERATOR


class TwoArityOperator(Operator, ABC):
    """
    This is a two-level operator.

    Modifies and mixes the original values using the `func` function.

    Has a `first_col`, `second_col` that generates the original value.
    """

    arity = 2
    suboperators: tuple[ZERO_ONE_OPERATOR]

    def __self_init__(self):
        self.shift = self.random.randint(0, 2)

    def __str_extra_args__(self) -> list[str]:
        return [f"shift={self.shift}"]

    @abstractmethod
    def formula(self, col_1: float, col_2: float) -> float:
        pass

    def func(self, first_col: COLOR_TYPE, second_col: COLOR_TYPE) -> COLOR_TYPE:
        """
        Color generation function. Accepts data for generation and
        outputs the first color step according to the described formula.
        """
        return (
            self.formula(first_col[0], second_col[(0 + self.shift) % 3]),
            self.formula(first_col[1], second_col[(1 + self.shift) % 3]),
            self.formula(first_col[2], second_col[(2 + self.shift) % 3]),
        )


# ======================================================================


class Sum(TwoArityOperator):
    """
    Calculates the average between the two colors.
    """
    def formula(self, col_1, col_2):
        return (col_1 + col_2) / 2


class Product(TwoArityOperator):
    """
    Multiplies one color by another.
    """
    def formula(self, col_1, col_2):
        return col_1 * col_2


class Mod(TwoArityOperator):
    """
    Calculates the mod of one color relative to another.
    """
    def formula(self, col_1, col_2):
        if col_2 == 0:
            return 0
        return col_1 % col_2


ZERO_ONE_TWO_OPERATOR = ZERO_ONE_OPERATOR | TwoArityOperator

__all__ = operator_subclass_names(locals())
