import re
from pathlib import Path
from argparse import ArgumentParser


__all__ = ["ImageManager"]


ROOT_PATH = Path(__file__).absolute().parent.parent.absolute()
DATA_DIR = Path('data')

ONLY_SYMBOLS = re.compile(r"[^a-zA-Zа-яА-ЯёЁ0-9\s]")


class ImageManager:
    def __init__(self):
        self.args = self.get_args()
        self.phrases = self.get_phrases()
        self.data_dir = self.get_data_dir()
        self.create_data_dir()

    @staticmethod
    def get_args():
        parser = ArgumentParser()
        parser.add_argument("-path", type=str)
        parser.add_argument("-target", type=str)
        parser.add_argument("-size", type=int, default=512)
        parser.add_argument("-deep", type=str)
        parser.add_argument("-phrase", type=str)

        return parser.parse_args()

    @staticmethod
    def read_file(root_path: str | Path) -> iter:
        root_path = Path(root_path)

        probable_paths = [root_path / "text", root_path / "text.txt", root_path]
        for text_path in probable_paths:
            if not text_path.is_file():
                continue
            with open(text_path, encoding='UTF-8') as file:
                text = file.read()
            if not text:
                continue
            return filter(None, text.splitlines())

        raise FileNotFoundError("no text file found")

    def get_phrases(self) -> iter:
        if self.args.phrase:
            return [self.args.phrase]

        if self.args.path:
            return self.read_file(self.args.path)

        return self.read_file(ROOT_PATH)

    def get_data_dir(self) -> Path:
        if self.args.target:
            target_dir = Path(self.args.target)
            if target_dir.is_absolute():
                return target_dir
        else:
            target_dir = DATA_DIR

        if self.args.path:
            root_dir = Path(self.args.path)
        else:
            root_dir = ROOT_PATH

        return root_dir / target_dir

    def create_data_dir(self):
        try:
            self.data_dir.mkdir()
        except FileExistsError:
            pass

    def create_folder(self, phrase: str) -> Path:
        dirname = ONLY_SYMBOLS.sub('', phrase)[:30]
        folder_path = Path()  # init for IDE

        is_created, add_num, num = False, '', 0
        while not is_created:
            folder_path = self.data_dir / (dirname + add_num)
            try:
                folder_path.mkdir()
                is_created = True
            except FileExistsError:
                num += 1
                add_num = '_{}'.format(num)

        return folder_path
