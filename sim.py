# Creates a self-selfSimilarity matrix from the user input
# and saves as matrix.png

import sys
import colorsys
import numpy as np
from PIL import Image, ImageDraw

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

    return words

# creates a 2D array, the first line and first column contains all the words in the song
# the 2D array is number_of_words + 1 X number_of_words + 1
def createNDArray(words):
    size = len(words)
    matrix = np.array(words)
    matrix = np.resize(matrix, (size + 1, size + 1))
    
    for i in range(size):
        matrix[0, i+1] = words[i]
        matrix[i+1, 0] = words[i]

    matrix[0, 0] = None
    
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            matrix[i, j] = False
    
    selfSimilarity(matrix)
    return matrix

# when x=y the value is set to True
def selfSimilarity(matrix):
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix)):
            if matrix[0, j] == matrix[i, 0]:
                matrix[i, j] = True

def colorizeImage(size, matrix, pixels, color):
    repeated_words = []
    for i in range(size):
        j = i + 1
        while j < size:
            if pixels[i, j] == color:
                if not (matrix[0, j + 1] in repeated_words): 
                    repeated_words.append(matrix[0, j + 1])
                j = size
            j += 1

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
                    index = repeated_words.index(matrix[0, j + 1])
                    pixels[i, j] = spectrum[index]
                except:
                    pass
    return pixels

# creates the self-similarity matrix
# (DEFAULT) mode='1' is a white and black version
# mode='RGB' is a colorized version
# (DEFAULT) dark=1 is white background with black/colorized pixels as words 
# dark=0 is black background with white/colorized pixels as words
def createImage(size, matrix, mode='RGB', dark=0):
    if mode == '1':
        img = Image.new(mode, (size, size), color=dark)
        pixels = img.load()
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                if matrix[i, j] == 'True':
                    pixels[i - 1, j - 1] = not dark

    if mode == 'RGB':
        if dark:
            dark = (255, 255, 255)
            color = (0, 0, 0)
        else:
            dark = (0, 0, 0)
            color = (255, 255, 255)
        img = Image.new(mode, (size, size), color=dark)
        pixels = img.load()
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                if matrix[i, j] == 'True':
                    pixels[i - 1, j - 1] = color

        pixels = colorizeImage(size, matrix, pixels, color)

    img = img.resize((size * 10, size * 10))
    img.save('matrix.png')

if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)

    words = getInput()
    print("\nYour song has {} words.".format(len(words)))

    matrix = createNDArray(words)

    createImage(len(words), matrix)
    print("Self-similarity matrix saved as: 'matrix.png'")
    

