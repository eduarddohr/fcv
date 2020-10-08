from tkinter import filedialog
import glob
import cv2
import os
import shutil
import numpy as np

def applyTransformations(imageToTransform, transformation, parameter):
    if transformation == "BoxFilter":
        kernel = np.ones((int(parameter), int(parameter)))
        kernel = kernel/ np.sum(kernel)
        return cv2.filter2D(imageToTransform, -1, kernel)
    elif transformation == "HighPass":
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        return cv2.filter2D(imageToTransform, -1, kernel)
    elif transformation == "Sharpenning":
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv2.filter2D(imageToTransform, -1, kernel)

directory = filedialog.askdirectory()
# print(directory)
if directory:
    imagesList = glob.glob(directory + "/*.jpg")
    newDir = directory + "_aug"
    if os.path.isdir(newDir):
        shutil.rmtree(newDir)
    os.mkdir(newDir)

    configFile = open(directory + "/config.txt")
    configFileLines = configFile.readlines()
    for line in configFileLines:
        option = line.split(':')
        counter = 1
        for imagePath in imagesList:
            image = cv2.imread(imagePath)
            imageName = imagePath.split("\\")
            imageName2 = imageName[-1].split(".")
            image = applyTransformations(image, option[0], option[1])
            cv2.imwrite(newDir + "/" + imageName2[0] + "_" + option[0] + "_" + str(counter) + ".jpg", image)
            counter += counter

else:
    print("dir does not exist")
