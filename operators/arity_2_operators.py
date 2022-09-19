"""
Operators with arity 2.

Take 2 colors and mix them in some way. Owns two 0/1 arity operators,
which calculate the initial colors.

Adds a shift by colors, that is, for two colors [rgb] + [RGB] can mix as
([rR gG bB], [rG gB bR], [rB gR bG]).
"""

from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE
from .arity_1_operators import ZERO_ONE_OPERATOR


class TwoArityOperator(Operator, ABC):
    """
    This is a two-level operator.

    Modifies and mix the original values using the formula from the
    `formula` method.

    Has two colors that were originally generated.
    """

    arity = 2
    suboperators: tuple[ZERO_ONE_OPERATOR]

    def __self_init__(self):
        self.shift = self.random.randint(0, 2)

    def __str_extra_args__(self) -> list[str]:
        return [f"shift={self.shift}"]

    @abstractmethod
    def formula(self, col_1: float, col_2: float) -> float:
        """
        The formula by which the two channels of colors are mixed.
        """
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
    Slightly decreases the brightness of the color because it mixed
    values.
    """
    def formula(self, col_1, col_2):
        return (col_1 + col_2) / 2.02


class Product(TwoArityOperator):
    """
    Multiplies one color by another.
    """
    def formula(self, col_1, col_2):
        return col_1 * col_2 / 1.0201


class Mod(TwoArityOperator):
    """
    Calculates the mod of one color relative to another.
    It decreases the brightness of the color, making it more like gray
    color (0.0), as it multiplies the fractional values by each other.
    """
    def formula(self, col_1, col_2):
        if col_2 == 0:
            return 0
        return col_1 % col_2


class Exponentiation(TwoArityOperator):
    """
    It changes the color by multiplying one color by a degree of
    another. The color sign is taken from the second color sign.
    It increases the brightness of the color, almost always giving
    brightness (< -0.5) | (> 0.5).
    """
    def formula(self, col_1, col_2):
        col_1 = min(abs(col_1), 1)
        if col_2 < 0:
            return - col_1 ** abs(col_2)
        else:
            return col_1 ** col_2


ZERO_ONE_TWO_OPERATOR = ZERO_ONE_OPERATOR | TwoArityOperator

__all__ = operator_subclass_names(locals())
