# Creates a self-selfSimilarity matrix from the user input
# and saves as matrix.png

import sys
import timeit
import colorsys
import numpy as np
from PIL import Image, ImageDraw
from graph import createGraph

# returns the formated user input: an array
def getInput():
    print("Press CTRL-Z and hit Enter to submit")
    ipt = sys.stdin.readlines()
    words = []
    for verse in ipt:
        word = ""
        for letter in verse:
            if letter == ' ' or letter == ',' or letter == '\n':    
                if len(word) > 0:
                    word = word.lower()
                    words.append(word)
                word = ""
            else:
                word += letter
    return np.array(words)

def colorizeImage(words, pixels, color):
    size = len(words)
    unique = np.unique(words, return_counts=True)
    repeated_words = [unique[0][i] for i in range(len(unique[0])) if unique[1][i] > 1]
    const = (360 / len(repeated_words))
    if color == (255, 255, 255):
        div = 360
    else:
        div = color[0]
    spectrum = []
    for i in range(len(repeated_words)):
        if color == (0, 0, 0):
            div += const
            c = colorsys.hsv_to_rgb(div/100, 1, 1)
            c = tuple([int(255 * x) for x in c])
            spectrum.append(c)
        else:
            div -= const
            c = colorsys.hsv_to_rgb(div/100, 1, 1)
            c = tuple([int(255 * x) for x in c])
            spectrum.append(c)
    for i in range(size):
        for j in range(size):
            if pixels[i, j] == color:
                try:
                    index = repeated_words.index(words[j])
                    pixels[i, j] = spectrum[index]
                except:
                    pass
    return pixels

# creates the self-similarity matrix
# (DEFAULT) mode='1' is a white and black version
# mode='RGB' is a colorized version
# (DEFAULT) dark=1 is white background with black/colorized pixels as words 
# dark=0 is black background with white/colorized pixels as words
def createImage(words, mode='RGB', dark=0):
    size = len(words)
    if mode == '1':
        img = Image.new(mode, (size, size), color=dark)
        pixels = img.load()
        for i in range(size):
            for j in range(size):
                if words[i] == words[j]:
                    pixels[i, j] = not dark

    if mode == 'RGB':
        if dark:
            dark = (255, 255, 255)
            color = (0, 0, 0)
        else:
            dark = (0, 0, 0)
            color = (255, 255, 255)
        img = Image.new(mode, (size, size), color=dark)
        pixels = img.load()
        for i in range(size):
            for j in range(size):
                if words[i] == words[j]:
                    pixels[i, j] = color
        pixels = colorizeImage(words, pixels, color)
    img = img.resize((size * 10, size * 10))
    img.save('matrix.png')

if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)

    words = getInput()
    print("\nYour song has {} words.".format(len(words)))

    start = timeit.default_timer()

    createImage(words)
    print("Self-similarity matrix saved as: 'matrix.png'")
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)

    createGraph(words)