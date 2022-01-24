"""
A manager for all operators, a class to inherit the rest of the
operators, and a couple of tools for easy code writing.
"""

from __future__ import annotations
from random import Random
from abc import ABC, ABCMeta, abstractmethod


__all__ = [
    "COLOR_TYPE",
    "OperatorManager",
    "Operator",
    "operator_subclass_names",
]


# Value in the range [-1; 1]
PIXEL_RANGE = float
COLOR_TYPE = tuple[PIXEL_RANGE, PIXEL_RANGE, PIXEL_RANGE]


class OperatorManager(ABCMeta):
    """
    A manager for all operators that generate image colors.

    Metaclass for all operators, but don't use it via
    `(metaclass=OperatorManager)`, instead inherit it from `Operator`
    class or its subclasses.
    Stores a list of all operators to generate, and passes the same
    instance of random to all objects to keep the generation identical.
    """

    arity: int
    _current_random: Random = Random()

    operators_flat: list[OperatorManager] = []
    operators_dimensional: list[OperatorManager] = []

    def __new__(mcs, clsname, bases, dct):
        cls = super().__new__(mcs, clsname, bases, dct)

        # Adding a new operator to the list of all operators
        if ABC not in bases:
            target_operators = (
                mcs.operators_dimensional
                if cls.arity > 0
                else mcs.operators_flat
            )
            target_operators.append(cls)

        return cls

    @classmethod
    def get_random(mcs) -> Random:
        """
        A method for getting a random object to all operators.
        """

        return mcs._current_random

    @classmethod
    def set_random(mcs, random_generator: Random):
        """
        A method for setting a random object to all operators.
        """

        mcs._current_random = random_generator

    @classmethod
    def get_operators_flat(mcs) -> list[OperatorManager]:
        """
        Sorted list of operators with `arity = 0`.
        """

        return sorted(mcs.operators_flat, key=lambda x: x.__name__)

    @classmethod
    def get_operators_dimensional(mcs) -> list[OperatorManager]:
        """
        Sorted list of operators with `arity > 0`.
        """

        return sorted(mcs.operators_dimensional, key=lambda x: x.__name__)


class Operator(ABC, metaclass=OperatorManager):
    """
    A class for inheriting all other operators.

    Only non-abstract subclasses (without ABC in parents) are used in
    image generation. If the class is non-abstract, it must have a
    complexity class `arity` (>= 0) and generation method `.eval()`.
    """

    arity: int
    suboperators: tuple[Operator]

    def __init__(self, *args: Operator):
        self.suboperators = args

    def __str_extra_args__(self) -> list[str]:
        """
        Converts to string form the additional arguments that are needed
        to duplicate the operator.
        """

        return []

    def __str__(self):
        args = (
            [str(sub_op) for sub_op in self.suboperators]
            + self.__str_extra_args__()
        )
        args_str = ", ".join(args)
        return f"{self.__class__.__name__}({args_str})"

    def as_str(self, sym="\t", _nesting: int = 0) -> str:
        indent = sym * _nesting

        args = [
            sub_op.as_str(sym=sym, _nesting=_nesting + 1)
            for sub_op in self.suboperators
        ]
        extra = [
            indent + sym + kwarg
            for kwarg in self.__str_extra_args__()
        ]

        args_str = ",\n".join(args + extra)
        if args_str:
            args_str = f"\n{args_str}\n{indent}"

        return f"{indent}{self.__class__.__name__}({args_str})"

    @classmethod
    @property
    def random(cls) -> Random:
        """
        A common instance of random from a metaclass.
        """

        return cls.__class__.get_random()

    @abstractmethod
    def func(self, *colors: COLOR_TYPE) -> COLOR_TYPE:
        """
        Generates color with its own suboperators and then passes the
        color calculation to its `func` function.
        """
        pass

    def eval(self, x: PIXEL_RANGE, y: PIXEL_RANGE) -> COLOR_TYPE:
        """
        Color generation based on the pixel's position relative to the
        center of the image.

        :param x: position on x
        :param y: position on y
        :return: rgb-color
        """

        colors = [sub_op.eval(x, y) for sub_op in self.suboperators]
        return self.func(*colors)


def operator_subclass_names(locals_: dict[str, object]) -> list[str]:
    """
    Function to get the names of all operators to be generated from the
    current file.

    :param locals_: `locals()` for the current module (not the built-in
        function, but the dictionary it returns)
    :return: list of names
    """

    def is_real_operator_subclass(name: str, cls: type) -> bool:
        """ Look only for non-abstract Operator subclasses. """
        return (
            isinstance(cls, OperatorManager)
            and ABC not in cls.__bases__
            and name == cls.__name__
        )

    return [
        name
        for (name, cls) in locals_.items()
        if is_real_operator_subclass(name, cls)
    ]
