# version 1.0.0

from implementers import *


def _get_deeps(preset_deep: str | int) -> list[int]:
    if preset_deep != "all":
        return [int(preset_deep)]

    deeps = [
        *range(1, Generator.deep_interval[0]),
        *range(*Generator.deep_interval, 2),
    ]
    return deeps


def main():
    image_manager = ImageManager()
    preset_deep = image_manager.args.deep
    generator = Generator(image_manager.args.size)

    for phrase in image_manager.phrases:
        deeps = _get_deeps(preset_deep or Generator.get_random_deep(phrase))

        dir_name = image_manager.create_folder(phrase)
        for deep in deeps:
            image_name = image_manager.data_dir / dir_name / f"{deep}.png"
            image = generator.generate_image(phrase, deep)
            image.save(image_name)

        print(f"phrase <{phrase}> has been generated")


if __name__ == "__main__":
    main()
