"""
A manager for all operators, a class to inherit the rest of the
operators, and a couple of tools for easy code writing.
"""

from __future__ import annotations
from random import Random
from abc import ABC, ABCMeta, abstractmethod
from typing import Type, Tuple


__all__ = [
    "COLOR_TYPE",
    "OperatorManager",
    "Operator",
    "operator_subclass_names",
]


# Value in the range [-1; 1]
PIXEL_RANGE = float
COLOR_TYPE = Tuple[PIXEL_RANGE, PIXEL_RANGE, PIXEL_RANGE]


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

    operators_flat: list[Type[Operator]] = []
    operators_dimensional: list[Type[Operator]] = []

    def __new__(mcs, clsname, bases, dct):
        cls: Type[Operator] = super().__new__(mcs, clsname, bases, dct)

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

    def __init__(self, *args: Operator, **kwargs):
        self.suboperators = args
        if not kwargs:
            self.__self_init__()
        else:
            # to get from the string
            for (name, value) in kwargs.items():
                setattr(self, name, value)

    def __self_init__(self):
        """
        Creates additional arguments that the operator needs.
        """
        pass

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

    def to_print(self, sym="\t", _nesting: int = 0) -> str:
        """
        A method similar to `.__str__()`, but returns the result in
        formatted form. It adds line breaks and indents.
        Parameter `sym` defines the indent, by default it is one tab,
        you can change it to spaces.
        """

        indent = sym * _nesting

        args = [
            sub_op.to_print(sym=sym, _nesting=_nesting + 1)
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

    @property
    def random(self) -> Random:
        """
        A common instance of random from a metaclass.
        """
        return self.__class__.__class__.get_random()

    def formula(self, *cols: float) -> float:
        pass

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
