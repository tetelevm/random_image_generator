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

    operators_plain = []
    operators_complex = []

    def __new__(mcs, clsname, bases, dct):
        cls = super().__new__(mcs, clsname, bases, dct)
        cls.random = classmethod(mcs._random_getter)

        if ABC not in bases:
            arr = mcs.operators_complex if cls.arity > 0 else mcs.operators_plain
            arr.append(cls)

        return cls

    @property
    def _random_getter(cls):
        return cls.__class__._current_random

    @classmethod
    def set_random(cls, random_generator):
        cls._current_random = random_generator

    @classmethod
    def get_operators_plain(self):
        return sorted(self.operators_plain, key=lambda x: x.sort_key)

    @classmethod
    def get_operators_complex(self):
        return sorted(self.operators_complex, key=lambda x: x.sort_key)


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
