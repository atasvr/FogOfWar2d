from random import random
from PIL import Image


class BlockMap(object):
    blocks = []

    def __init__(self, gridSize, realSize):
        self.size = gridSize
        self.realSize = realSize
        self.blocks = [0] * gridSize * gridSize
        self.GenerateMapToImage()


    def GenerateRandomMap(self):
        size = self.size * self.size
        self.blocks = [0] * size

        for i in range(size):
            if random() < 0.5:
                self.blocks[i] = 1

    def GetBlock(self, position):
        return self.blocks[position[0] + (self.size * position[1])]

    def GenerateMapToImage(self):
        img = Image.open('Images/BlockMap.png')
        size = self.size * self.size
        imgHeight = img.height - 1
        imgWidth = img.width - 1
        print((imgHeight, imgWidth))
        for i in range(size):
            x = (i - (i % self.size)) / self.size
            y = i % self.size
            #print((round(imgHeight * (x/self.size))), round(imgWidth * (y/self.size)))
            pixel = img.getpixel((round(imgWidth * (y/self.size)), round(imgHeight * (x/self.size))))
            if pixel == None:
                continue

            if pixel[0] < 200:
                self.blocks[i] = 1
                print(pixel[0])

