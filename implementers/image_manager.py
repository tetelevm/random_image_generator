"""
The main manager of the system job.

Reads arguments, gets the necessary phrases, creates folders and the like.
"""

import re
from pathlib import Path
from typing import Iterable
from argparse import ArgumentParser, Namespace


__all__ = ["ImageManager"]


# Directory with `randomart.py`
ROOT_PATH = Path(__file__).absolute().parent.parent.absolute()

# English and Russian, another language can be added if necessary
ONLY_SYMBOLS = re.compile(r"[^a-zA-Zа-яА-ЯёЁ0-9\s]")


class ImageManager:
    """
    A manager which is responsible for handling image files, and is also
    responsible for startup parameters.

    It has methods for getting startup arguments, reading text, creating
    folders.
    """

    def __init__(self):
        self.args = self.get_args()
        self.phrases = self.get_phrases()
        self.data_dir = self.get_data_dir()
        self.create_data_dir()

    @staticmethod
    def get_args() -> Namespace:
        """
        A method that declares all possible startup arguments and reads
        them.

        Available arguments:
        - `path`
            The path to the default directory. The directory must contain
            the file 'text'/'text.txt' (although `path` can also point
            directly to the file). The default directory is where
            randomart.py is.
        - `target`
            Path to the target directory where the images will
            be generated. Can be absolute or just a name (then applied
            to `path`). The default is 'data'.
        - `size`
            The size of the resulting images. The larger the size, the
            longer the image is generated, the default is 512x512 pixels.
        - `complexity`
            The complexity of the art. By default it is taken from the
            phrase, but can be set manually as an integer or as the word
            `all`.
        - `phrase`
            The phrase by which the image is generated. If specified, it
            generates by it, else it tries to read the phrase file.

        :return: object with arguments
        """

        parser = ArgumentParser()
        parser.add_argument("-path", type=str)
        parser.add_argument("-target", type=str, default="data")
        parser.add_argument("-size", type=int, default=512)
        parser.add_argument("-complexity", type=str)
        parser.add_argument("-phrase", type=str)

        return parser.parse_args()

    @staticmethod
    def read_file(root_path: str | Path) -> Iterable[str]:
        """
        Searches and reads the phrase file.

        Searches for files by the passed path as
        ['{PATH}/text', '{PATH}/text.txt', '{PATH}'].
        That is, the path must be either a file or a directory with the
        `text`/`text.txt` file inside. If the file is not found, it
        raises FileNotFoundError exception. If file is found, it reads
        it, splits it into lines and returns all nonempty lines.

        :param root_path: the path to the directory with the file or file
        :return: phrases from the file
        """

        root_path = Path(root_path)

        probable_paths = [root_path / "text", root_path / "text.txt", root_path]
        for text_path in probable_paths:
            if not text_path.is_file():
                continue
            with open(text_path, encoding="UTF-8") as file:
                text = file.read()
            if not text:
                continue
            return filter(None, text.splitlines())

        raise FileNotFoundError("no text file found")

    def get_phrases(self) -> Iterable[str]:
        """
        Returns an iterable object of phrases that should be used to
        generate images.

        If the `-phrase` argument was passed when the script was started,
        the generation is based only on it, if not, the phrase file is
        searched and the phrases are taken from there (see
        `.read_file()`).

        :return: phrases to generate
        """

        if self.args.phrase:
            return [self.args.phrase]

        if self.args.path:
            return self.read_file(self.args.path)

        return self.read_file(ROOT_PATH)

    def get_data_dir(self) -> Path:
        """
        Attempts to define a directory for the generated images.

        If `target_dir` is specified as an absolute path, it is used. If
        `target_dir` is relative or not specified (then 'data'), then
        `path` is used as the parent directory.

        :return: directory path
        """

        target_dir = Path(self.args.target)
        if target_dir.is_absolute():
            return target_dir

        root_dir = Path(self.args.path) if self.args.path else ROOT_PATH
        root_dir = root_dir.absolute()
        if root_dir.is_file():
            root_dir = root_dir.parent

        return root_dir / target_dir

    def create_data_dir(self):
        """
        Creates a directory for the generated images if it is missing.
        """

        try:
            self.data_dir.mkdir()
        except FileExistsError:
            pass

    def create_folder(self, phrase: str) -> Path:
        """
        Creates directories for images.

        Removes from the phrase all the characters that could interfere
        with the creation of the directory (punctuation marks, special
        characters, etc.), cuts off long phrases and creates the
        directory. If one already exists, it appends '_1', '_2', ... .
        Uses `self.data_dir` as root directory (see `.get_data_dir()`).

        :param phrase: the phrase by which the image is generated
        :return: path to the created directory
        """

        dirname = ONLY_SYMBOLS.sub("", phrase)[:30]
        folder_path = Path()  # init for IDE,  will be overwritten

        is_created, add_num, num = False, "", 0
        while not is_created:
            folder_path = self.data_dir / (dirname + add_num)
            try:
                folder_path.mkdir()
                is_created = True
            except FileExistsError:
                num += 1
                add_num = "_{}".format(num)

        return folder_path  # absolute path
