# version 1.0.9

"""
The entry point to the generator.
Responsible for the interaction of the other parts of the system.
"""

from implementers import *


def _get_complexities(preset_complexity: str | int) -> list[int]:
    if preset_complexity != "all":
        return [int(preset_complexity)]

    complexities = [
        *range(1, Generator.complexity_interval[0]),
        *range(*Generator.complexity_interval, 2),
    ]
    return complexities


def main():
    image_manager = ImageManager()
    input_complexity = image_manager.args.complexity
    generator = Generator(image_manager.args.size)

    for phrase in image_manager.phrases:
        preset_complexity = input_complexity or Generator.get_complexity(phrase)
        complexities = _get_complexities(preset_complexity)

        dir_name = image_manager.create_folder(phrase)
        for complexity in complexities:
            image_name = dir_name / f"{complexity}.png"
            image = generator(phrase, complexity)
            image.save(image_name)

        print(f"phrase <{phrase}> has been generated into <{dir_name.name}>")


if __name__ == "__main__":
    main()
