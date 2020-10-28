from tkinter import filedialog
import glob
import cv2
import os
import shutil
import numpy as np


def BoxFilter(imageToTransform, parameter):
    kernel = np.ones((int(parameter), int(parameter)))
    kernel = kernel / np.sum(kernel)
    return cv2.filter2D(imageToTransform, -1, kernel)


def HighPass(imageToTransform, parameter):
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    return cv2.filter2D(imageToTransform, -1, kernel)


def Sharpening(imageToTransform, parameter):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(imageToTransform, -1, kernel)


def Rotate(imageToTransform, angle):
    image_center = tuple(np.array(imageToTransform.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, int(angle), 1.0)
    result = cv2.warpAffine(imageToTransform, rot_mat, imageToTransform.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def Translate(image, parameters):
    height, width = image.shape[:2]
    translation = np.float32([[1, 0, parameters[0]], [0, 1, parameters[1]]])
    return cv2.warpAffine(image, translation, (width, height))


def Shear(image, parameters):
    height, width = image.shape[:2]
    translation = np.float32([[1, parameters[0], 0], [parameters[1], 1, 0]])
    return cv2.warpAffine(image, translation, (width, height))


def Flip(image, parameters):
    return cv2.flip(image, int(parameters[0]))


def applyTransformations(imageToTransform, transformation, parameter):
    if transformation == "BoxFilter":
        return BoxFilter(imageToTransform, parameter[0])
    elif transformation == "HighPass":
        return HighPass(imageToTransform, parameter[0])
    elif transformation == "Sharpening":
        return Sharpening(imageToTransform, parameter[0])
    elif transformation == "Rotate":
        return Rotate(imageToTransform, parameter[0])
    elif transformation == "Translate":
        return Translate(image, parameter)
    elif transformation == "Shear":
        return Shear(image, parameter)
    elif transformation == "Flip":
        return Flip(image, parameter)


directory = filedialog.askdirectory()
# print(directory)
if directory:
    imagesList = glob.glob(directory + "/*.jpg")
    newDir = directory + "_aug"
    appliedTransformations = ""
    if os.path.isdir(newDir):
        shutil.rmtree(newDir)
    os.mkdir(newDir)

    configFile = open(directory + "/config.txt")
    configFileLines = configFile.readlines()
    for line in configFileLines:
        counter = 1
        for imagePath in imagesList:
            image = cv2.imread(imagePath)
            imageName = imagePath.split("\\")
            imageName2 = imageName[-1].split(".")
            appliedTransformations = ""
            options = line.split(';')
            for op in options:
                option = op.split(':')
                parameters = option[1].split(',')
                image = applyTransformations(image, option[0], parameters)
                appliedTransformations += option[0] + "_"
            cv2.imwrite(newDir + "/" + imageName2[0] + "_" + appliedTransformations + str(counter) + ".jpg", image)
            counter += counter

else:
    print("dir does not exist")
