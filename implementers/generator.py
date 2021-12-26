"""
Image generator.

Contains all the generation logic: creates art of operators and itself
generates a picture.
"""

from random import Random
from PIL import Image

from operators import OperatorManager, Operator


__all__ = ["Generator"]


class Generator:
    operators_flat = OperatorManager.get_operators_flat()
    operators_dimensional = OperatorManager.get_operators_dimensional()
    complexity_interval = [20, 150]

    def __init__(self, size: int = 256):
        self.size = size
        self.random = Random()

    @classmethod
    def get_complexity(cls, phrase: str) -> int:
        random_local = Random(phrase)
        return random_local.randint(*cls.complexity_interval)

    @classmethod
    @property
    def all_complexities(cls) -> list[int]:
        return [
            *range(1, cls.complexity_interval[0]),
            *range(*cls.complexity_interval, 2),
        ]

    def __call__(self, phrase: str, complexity: int) -> Image:
        self.random = Random(phrase)
        OperatorManager.set_random(self.random)
        art = self.generate_art(complexity)
        return self.draw(art)

    def generate_art(self, complexity: int) -> Operator:
        if complexity <= 0:
            plain_operator = self.random.choice(self.operators_flat)
            return plain_operator()

        operator = self.random.choice(self.operators_dimensional)
        sub_complexities = [
            self.random.randrange(complexity)
            for _ in range(operator.arity - 1)
        ]

        suboperators = []
        last_complexity = 0
        for curr_complexity in sorted(sub_complexities):
            suboperator = self.generate_art(curr_complexity - last_complexity)
            suboperators.append(suboperator)
            last_complexity = curr_complexity

        suboperators.append(self.generate_art(complexity - 1 - last_complexity))

        return operator(*suboperators)

    @staticmethod
    def normalize_color(r: float, g: float, b: float) -> tuple[int, int, int]:
        to_col = lambda x: max(1, min(255, int(128 * (x + 1))))
        return (to_col(r), to_col(g), to_col(b))

    def draw(self, art: Operator) -> Image:
        img = Image.new("RGB", (self.size, self.size))
        for x in range(self.size):
            for y in range(self.size):
                rgb = art.eval(
                    2 * x / self.size - 1,
                    2 * y / self.size - 1,
                )
                img.putpixel((x, y), self.normalize_color(*rgb))

        return img
