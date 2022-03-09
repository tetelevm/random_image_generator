"""
Operators with arity 3.

Take 3 colors and mix them in some way. Own the three 0/1/2 arity
operators, which calculate the original colors. The second and third
colors are mixed, and the third comes as a filter for them.

In this version the values (r, g, b) do not intersect each other and are
calculated separately, but this will change in the future (and is more
of a bug right now).
"""

from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE
from .arity_2_operators import ZERO_ONE_TWO_OPERATOR


class ThreeArityOperator(Operator, ABC):
    """
    This is a three-level operator.

    Modifies and mixes the values from the suboperators using the
    mathematical formula described in the `func` function.

    Has three suboperators that calculate the original color values.
    """

    arity = 3
    suboperators: tuple[ZERO_ONE_TWO_OPERATOR]

    def __self_init__(self):
        self.shift = self.random.randint(0, 2)

    def __str_extra_args__(self) -> list[str]:
        return [f"shift={self.shift}"]

    @abstractmethod
    def formula(self, col_1: float, col_2: float, col_3: float) -> float:
        pass

    def func(
            self,
            first_col: COLOR_TYPE,
            second_col: COLOR_TYPE,
            third_col: COLOR_TYPE
    ) -> COLOR_TYPE:
        """
        Color generation function. Accepts data for generation and
        outputs the first color step according to the described formula.
        """

        r = self.formula(
            first_col[0],
            second_col[(0 + self.shift) % 3],
            third_col[(0 + self.shift * 2) % 3],
        )
        g = self.formula(
            first_col[1],
            second_col[(1 + self.shift) % 3],
            third_col[(1 + self.shift * 2) % 3],
        )
        b = self.formula(
            first_col[2],
            second_col[(2 + self.shift) % 3],
            third_col[(2 + self.shift * 2) % 3],
        )
        return (r, g, b)


# ======================================================================


class Level(ThreeArityOperator):
    """
    Selects one of two colors depending on the value of the third color.
    """

    def __self_init__(self):
        super().__self_init__()
        self.treshold = self.random.uniform(-1.0, 1.0)

    def __str_extra_args__(self):
        return super().__str_extra_args__() + [f"treshold={self.treshold}"]

    def formula(self, col_1, col_2, col_3):
        return col_1 if col_2 < self.treshold else col_3


class Mix(ThreeArityOperator):
    """
    Calculates the average between the two colors (must initially mix
    these colors with a third color).
    """

    def formula(self, col_1, col_2, col_3):
        w = 0.5 * (col_1 + 1.0)
        return w * col_2 + (1 - w) * col_3


class LineAvg(ThreeArityOperator):
    def formula(self, col_1, col_2, col_3):
        mi, av, ma = sorted([col_1, col_2, col_3])
        if ma - mi == 0:
            return 0.0
        return (ma + mi - 2 * av) / (ma - mi)


ZERO_ONE_TWO_THREE_OPERATOR = ZERO_ONE_TWO_OPERATOR | ThreeArityOperator

__all__ = operator_subclass_names(locals())
