from random import Random
from PIL import Image

from operators import OperatorManager


__all__ = ["Generator"]


class Generator:
    operators_plain = OperatorManager.get_operators_plain()
    operators_complex = OperatorManager.get_operators_complex()
    deep_interval = [20, 150]

    def __init__(self, size: int = 256):
        self.size = size
        self.random = Random()

    @classmethod
    def get_random_deep(cls, phrase: str) -> int:
        random_local = Random(phrase)
        return random_local.randint(*cls.deep_interval)

    def generate_image(self, phrase: str, deep: int) -> Image:
        self.random = Random(phrase)
        OperatorManager.set_random(self.random)
        art = self.generate_art(deep)

        return self.draw(art)

    def generate_art(self, deep):
        if deep <= 0:
            plain_operator = self.random.choice(self.operators_plain)
            return plain_operator()

        operator = self.random.choice(self.operators_complex)
        i = 0
        args = []

        ops = [self.random.randrange(deep) for _ in range(operator.arity - 1)]
        for j in sorted(ops):
            args.append(self.generate_art(j - i))
            i = j
        args.append(self.generate_art(deep - 1 - i))
        return operator(*args)

    @staticmethod
    def normalize_color(r, g, b):
        val = lambda x: max(1, min(255, int(128 * (x + 1))))
        return (val(r), val(g), val(b))

    def draw(self, art) -> Image:
        img = Image.new('RGB', (self.size, self.size))
        for x in range(self.size):
            for y in range(self.size):
                rgb = art.eval(
                    2 * x / self.size - 1,
                    2 * y / self.size - 1,
                )
                img.putpixel((x, y), self.normalize_color(*rgb))

        return img
