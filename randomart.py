# version 1.0.0

from implementers import *


def main():
    image_manager = ImageManager()
    preset_deep = image_manager.args.deep
    generator = Generator(image_manager.args.size)

    for phrase in image_manager.phrases:
        if preset_deep:
            deep = preset_deep
        else:
            deep = generator.get_random_deep(phrase)

        folder_path = image_manager.create_folder(phrase)
        image = generator.generate_image(phrase, deep)
        image_path = image_manager.data_dir / folder_path / f"{deep}.png"
        image.save(image_path)
        print(f"phrase <{phrase}> has been generated")


if __name__ == "__main__":
    main()
