"""
Image generator.

Contains all the generation logic: creates art of operators and itself
generates a picture.
"""

from random import Random
from PIL import Image

from operators import *


__all__ = ["Generator"]


class Generator:
    """
    A class that generates art by phrase and an image by art.

    Art is a group of operators that generates the color of a pixel
    depending on its position. In essence, art is a formula with a large
    nesting of operators that takes two values of the range [-1; 1] as
    input, and returns three similar values as output. The art is the
    same for all pixels, and its complexity determines the complexity
    and appearance of the image.
    For each pixel of the image an art calculation is applied, so there
    is a linear relationship between the count of pixels and generation
    time. The value of the pixel position is taken as
    `2 * pos / size - 1`, that is, at the beginning -1, in the center 0,
    at the end 1.
    When generating an image, sets a certain state of the random
    generator depending on the phrase and passes it to all operators.
    """

    operators_flat = OperatorManager.get_operators_flat()
    operators_dimensional = OperatorManager.get_operators_dimensional()
    complexity_interval = [20, 150]

    def __init__(self, size: int = 256):
        self.size = size
        self.random = Random()

    @classmethod
    def get_complexity(cls, phrase: str) -> int:
        """
        Random selection of complexity depending on the phrase.
        """

        random_local = Random(phrase)
        return random_local.randint(*cls.complexity_interval)

    @classmethod
    @property
    def all_complexities(cls) -> list[int]:
        """
        Default complexities for generating images on all complexities.
        """

        return [
            *range(1, cls.complexity_interval[0]),
            *range(*cls.complexity_interval, 2),
        ]

    def create_image(self, phrase: str, complexity: int, size=None) -> Image:
        """
        Sets the state of random, generates art and with it the image.
        """

        self.random = Random(phrase)
        OperatorManager.set_random(self.random)
        art = self.generate_art(complexity)
        size = size or self.size
        return self.draw(art, size)

    def generate_art(self, complexity: int) -> Operator:
        """
        Art generation method.

        The art is generated recursively. First an operator is chosen,
        and then suboperators are generated to it (if `complexity = 0`,
        it just returns a plain operator).
        The operator is chosen randomly from a list of all operators.
        Suboperators are necessarily less complex than the operator. All
        but one of the random operators are generated first, and then
        the last one of slightly less complexity than the original
        complexity.
        """

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
    def read_art(art_string: str) -> Operator:
        """
        Creates art from its string representation.

        It is expected that `art_string` will look like `str(art)`, that
        is, it will contain operator names, nested operators as `*args`
        and internal operator variables as `**kwargs`.
        Made so you can share art or experiment with it.
        """

        return eval(art_string)

    @staticmethod
    def normalize_color(r: float, g: float, b: float) -> tuple[int, int, int]:
        """
        Converts the color from the range [-1; 1] to the standard
        [0; 255].
        """
        to_col = lambda x: max(1, min(255, int(128 * (x + 1))))
        return (to_col(r), to_col(g), to_col(b))

    @classmethod
    def draw(cls, art: Operator, size: int) -> Image:
        """
        Executes the art for each pixel and sets the resulting value in
        the image.
        """

        img = Image.new("RGB", (size, size))

        # Although a pixel is a rectangle rather than a dot, it is colored like
        # the dot in the upper left corner.
        for x in range(size):
            for y in range(size):
                x_pos = 2 * x / size - 1
                y_pos = 2 * y / size - 1
                rgb = art.eval(x_pos, y_pos)
                img.putpixel((x, y), cls.normalize_color(*rgb))

        return img
