# Random Image Generator

**Random Image Generator** is a simple program that generates an image by a
given phrase. Example:

![img.png](img.png "Phrase for the image (complexity 138)")

## Description

This was originally a script [translated][original] from OCalm to Python.
Little changes have been made here:

- the code is made more clear for easy modification

- the program uses `PIL` to display the pixels

- added shell arguments

- added new operators


The idea of generation is to create an art and then calculate it. Art is a huge
formula with a large nesting of operators. Operator is some mathematical
expression (e.g., sinus) that converts 3 channels of the original color into 3
channels of the new color. After creating the art, each pixel's color is
calculated according to a given formula. The channel value can be in the range
[-1; 1].

Art is always applied equally to any pixel. That is, there is no place for
random values in the art if they are generated during the calculation of the
art, but you can if the values are generated during creation. Ideally, the art
should be able to be output as a string.

There is [a brief article][article] that describes how it works (the article
is in Russian).

## Running

This version is written for Python3.10, but it can easily be downgraded to
Python3.7 simply by removing the type annotations. The simplest example of
running the generator:

```
python3.10 main.py
```

This will generate several 512x512 px images (one in each folder) from the
phrases written in the `text.txt` file in the generator directory. The run
supports some arguments:

- `path` -  the path to the default directory. The directory must contain the
file 'text'/'text.txt' (although `path` can also point directly to the file).
The default directory is where `main.py` is.

- `target` - path to the target directory where the images will be generated.
Can be absolute or just a name (then applied to `path`). The default is 'data'.

- `size` - the size of the resulting images. The larger the size, the longer
the image is generated, the default is 512x512 pixels.

- `complexity` - the complexity of the art. By default, it is taken from the
phrase, but can be set manually as an integer or as the word `all`.

- `phrase` - the phrase by which the image is generated. If specified, it
generates by it, else it tries to read the phrase file.

Example of a more complex generator start:

```
python3.10 main.py \
    -size 512 -phraze "Universe Great Love" \
    -complexity 100 \
    -path /home/user/randomart \
    -target images
```

[original]: http://math.andrej.com/2010/04/21/random-art-in-python/
[article]: https://github.com/tetelevm/articles/blob/main/russian/%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80_%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9/%D1%81%D1%82%D0%B0%D1%82%D1%8C%D1%8F.md
