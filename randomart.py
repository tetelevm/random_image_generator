# version 1.1.1

"""
The entry point to the generator.
Responsible for the interaction of the other parts of the system.
"""

from implementers import *


def main():
    """
    The main function of the system, which creates all images by given
    phrases with input (or calculated) complexities.
    """

    image_manager = ImageManager()
    generator = Generator(image_manager.args.size)

    if image_manager.args.complexity == "all":
        input_complexities = Generator.all_complexities
    elif image_manager.args.complexity is not None:
        input_complexities = [int(image_manager.args.complexity)]
    else:
        input_complexities = None

    for phrase in image_manager.phrases:
        complexities = input_complexities or [Generator.get_complexity(phrase)]

        dir_name = image_manager.create_folder(phrase)
        for complexity in complexities:
            image_name = dir_name / f"{complexity}.png"
            image = generator(phrase, complexity)
            image.save(image_name)

        print(f"phrase <{phrase}> has been generated into <{dir_name.name}>")


if __name__ == "__main__":
    main()
