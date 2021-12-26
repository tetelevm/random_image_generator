"""
A manager for all operators, a class to inherit the rest of the operators,
and a couple of tools for easy code writing.
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


COLOR_TYPE = tuple[float, float, float]


class OperatorManager(ABCMeta):
    arity: int
    _current_random: Random = Random()

    operators_flat: list[OperatorManager] = []
    operators_dimensional: list[OperatorManager] = []

    def __new__(mcs, clsname, bases, dct):
        cls = super().__new__(mcs, clsname, bases, dct)

        # A confusing and obscure hack for calling the same object of random
        # from all operators
        cls.random = classmethod(mcs._random_getter)

        if ABC not in bases:
            target_operators = (
                mcs.operators_dimensional
                if cls.arity > 0
                else mcs.operators_flat
            )
            target_operators.append(cls)

        return cls

    @property
    def _random_getter(cls):
        return cls.__class__._current_random

    @classmethod
    def set_random(cls, random_generator):
        cls._current_random = random_generator

    @classmethod
    def get_operators_flat(self) -> list[OperatorManager]:
        return sorted(self.operators_flat, key=lambda x: x.sort_key)

    @classmethod
    def get_operators_dimensional(self) -> list[OperatorManager]:
        return sorted(self.operators_dimensional, key=lambda x: x.sort_key)


class Operator(ABC, metaclass=OperatorManager):
    arity: int
    random: Random

    # To sort as in the original, the first change will delete
    sort_key: int

    @abstractmethod
    def eval(self, x: float, y: float) -> COLOR_TYPE:
        pass


def operator_subclass_names(locals_: dict[str, object]) -> list[str]:
    def is_operator_subclass(cls) -> bool:
        return isinstance(cls, OperatorManager) and ABC not in cls.__bases__

    return [
        name
        for (name, cls) in locals_.items()
        if not name.startswith("_") and is_operator_subclass(cls)
    ]
