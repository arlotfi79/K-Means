###############################################################
#                  ***k-means Clustering***
# authors : Alireza Lotfi (CSE Shiraz University) , Abdollah Hesami (CSE Shiraz University)
# date : Saturday, 30 January 2021
###############################################################

import cv2
import numpy as np
import random
import time

MAX_ITERATIONS = 100
start = time.time()
counter = 0


###############################################################

def distance2(pixel, pixel_tar, n=None):
    under_root = 0
    for i in range(2, 5):
        under_root += abs(int(pixel_tar[i]) - int(pixel[i]))
    return under_root


###############################################################

def findClosestCentroid(centroids, point, n=2):
    return_val = 0
    distance_val = distance(point, centroids[0], n)
    for i in range(len(centroids)):
        if distance(point, centroids[i], n) < distance_val:
            return_val = i
    return return_val


###############################################################

def updateCentroid(centroidElements, centroid):
    summation = [-1, -1, 0, 0, 0]
    n = len(centroidElements)
    if n == 0:
        return centroid
    for centroidElement in centroidElements:
        for i in range(2, 5):
            summation[i] += centroidElement[i]
    return [-1, -1, summation[2] // n, summation[3] // n, summation[4] // n]


###############################################################

def distance(pixel, pixel_tar, n=2):
    under_root = 0
    for i in range(2, 5):
        under_root += (abs(int(pixel_tar[i]) - int(pixel[i]))) ** n
    return under_root ** (1 / n)


###############################################################

def Stop(oldCentroids, centroids, iterations):
    if iterations > MAX_ITERATIONS:
        return True
    return oldCentroids == centroids


###############################################################

def makePicture(pic):
    img1 = []
    img2 = []
    row = pic[-1][0] + 1
    col = pic[-1][1] + 1
    for i in range(row):
        for j in range(col):
            andis = i * col + j
            img1 += [[np.uint8(pic[andis][4]), np.uint8(pic[andis][3]), np.uint8(pic[andis][2])]]
        img2 += [img1]
        img1 = []
    return np.array(img2)


###############################################################

def getPicture(filename):
    img = cv2.imread(filename)
    lis = img.shape
    piclist = []
    row = lis[0]
    col = lis[1]
    for i in range(row):
        for j in range(col):
            pix_b = img[i][j][0]
            pix_g = img[i][j][1]
            pix_r = img[i][j][2]
            piclist += [[i, j, pix_r, pix_g, pix_b]]
    return piclist


###############################################################

def kMeansClustering(k, picture, dis_pow=2):
    global counter
    centroids = [
        [-1, -1, np.uint8(random.randint(0, 255)), np.uint8(random.randint(0, 255)), np.uint8(random.randint(0, 255))]
        for _ in range(k)]
    rows, cols = picture[-1][0] + 1, picture[-1][1] + 1
    oldCentroids = []
    iterations = 0

    while not Stop(oldCentroids, centroids, iterations):
        counter += 1
        oldCentroids = centroids
        iterations += 1

        centroidElements = []

        for i in range(k):
            centroidElements += [[]]
        num_pixel = len(picture)

        for i in range(num_pixel):
            index = findClosestCentroid(centroids, picture[i], dis_pow)
            centroidElements[index] += [picture[i]]
        centroids = [updateCentroid(centroidElements[i], centroids[i]) for i in range(k)]

    for i in range(k):
        for j in range(len(centroidElements[i])):
            for m in range(2, 5):
                centroidElements[i][j][m] = centroids[i][m]

    new_picture = []
    for i in range(rows * cols):
        new_picture += [[]]
    for i in range(k):
        for j in range(len(centroidElements[i])):
            index = centroidElements[i][j][0] * cols + centroidElements[i][j][1]
            new_picture[index] = centroidElements[i][j]

    return new_picture


###############################################################################


k = int(input('Enter value of k : '))
picture_name = input('\nEnter picture\'s name : ')
print('calculating ...')
picture_code = getPicture(picture_name)
pic_code_two = kMeansClustering(k, picture_code[:])
image = makePicture(pic_code_two)
cv2.imwrite('k-means_' + picture_name + '.png', image)
cv2.imshow('image', image)
print(time.time() - start)
print(counter)
print('finish')
cv2.waitKey(5000)
