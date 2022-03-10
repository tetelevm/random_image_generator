"""
Operators with arity 3.

Take 3 colors and mix them in some way. Own the three 0/1/2 arity
operators, which calculate the original colors. The second and third
colors are mixed, and the third comes as a filter for them.

Adds a shift by colors, that is, for three colors [rgb] + [RGB] + [`r`g`b]
can mix as ([rR`r gG`g bB`b], [rG`b gB`r bR`g], [rB`g gR`b bG`r]).
"""

from abc import ABC, abstractmethod

from .base import Operator, operator_subclass_names, COLOR_TYPE
from .arity_2_operators import ZERO_ONE_TWO_OPERATOR


class ThreeArityOperator(Operator, ABC):
    """
    This is a three-level operator.

    Modifies and mix the original values using the formula from the
    `formula` method.

    Has three colors that were originally generated.
    """

    arity = 3
    suboperators: tuple[ZERO_ONE_TWO_OPERATOR]

    def __self_init__(self):
        self.shift = self.random.randint(0, 2)

    def __str_extra_args__(self) -> list[str]:
        return [f"shift={self.shift}"]

    @abstractmethod
    def formula(self, col_1: float, col_2: float, col_3: float) -> float:
        """
        The formula by which the three channels of colors are mixed.
        """
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
    Mixes two colors in proportions of the third color.
    """
    def formula(self, col_1, col_2, col_3):
        w = 0.5 * (col_1 + 1.0)
        return w * col_2 + (1 - w) * col_3


class LineAvg(ThreeArityOperator):
    """
    Draws a decreasing line through the coordinates (-1 x, max_color y)
    and (1 x, min_color y) and finds the x-location of y-avg_color on it.
    """
    def formula(self, col_1, col_2, col_3):
        mi, av, ma = sorted([col_1, col_2, col_3])
        if ma - mi == 0:
            # if all colors are the same
            return 0.0
        return (ma + mi - 2 * av) / (ma - mi)


ZERO_ONE_TWO_THREE_OPERATOR = ZERO_ONE_TWO_OPERATOR | ThreeArityOperator

__all__ = operator_subclass_names(locals())
