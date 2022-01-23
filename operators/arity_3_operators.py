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

    @abstractmethod
    def func(
            self,
            first_col: COLOR_TYPE,
            second_col: COLOR_TYPE,
            third_col: COLOR_TYPE
    ) -> COLOR_TYPE:
        pass


# ======================================================================


class Level(ThreeArityOperator):
    """
    Selects one of two colors depending on the value of the third color.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.treshold = self.random.uniform(-1.0, 1.0)

    def func(self, first_col, second_col, third_col):
        r = second_col[0] if first_col[0] < self.treshold else third_col[0]
        g = second_col[1] if first_col[1] < self.treshold else third_col[1]
        b = second_col[2] if first_col[2] < self.treshold else third_col[2]
        return (r, g, b)


class Mix(ThreeArityOperator):
    """
    Calculates the average between the two colors (must initially mix
    these colors with a third color).
    """

    def func(self, first_col, second_col, third_col):
        w = 0.5 * (first_col[0] + 1.0)

        r = w * second_col[0] + (1 - w) * third_col[0]
        g = w * second_col[1] + (1 - w) * third_col[1]
        b = w * second_col[2] + (1 - w) * third_col[2]
        return (r, g, b)


ZERO_ONE_TWO_THREE_OPERATOR = ZERO_ONE_TWO_OPERATOR | ThreeArityOperator

__all__ = operator_subclass_names(locals())
