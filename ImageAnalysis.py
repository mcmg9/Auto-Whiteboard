import imageio
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import sys

import skimage
import skimage.feature
import skimage.viewer
from skimage.transform import resize

from PIL import Image, ImageOps
from tsp_solver.greedy_numpy import solve_tsp
from scipy.spatial.distance import pdist, squareform

import serial

from time import sleep

#py -3 .\ImageAnalysis.py IMAGELINK

filename = sys.argv[1]
sigma = 2.5
low_threshold = 0.1
high_threshold = 0.3

image = skimage.io.imread(fname=filename, as_gray=True)
image_resized = resize(image, (160, 160), anti_aliasing=True)

edges = skimage.feature.canny(
    image=image_resized,
    sigma=sigma,
    low_threshold=low_threshold,
    high_threshold=high_threshold,
)

skimage.io.imsave("newimg.jpg", edges) 

print("Converting image to path...")

im = Image.open('newimg.jpg')
im_invert = ImageOps.invert(im)
im_invert.save('newimg.jpg', quality=95)

original_image = Image.open('newimg.jpg')
bw_image = original_image.convert('1', dither=Image.NONE)

bw_image_array = np.array(bw_image, dtype=int)
black_indices = np.argwhere(bw_image_array == 0)
#chosen_black_indices = black_indices[np.random.choice(black_indices.shape[0], replace=False, size=int(len(black_indices)))]

distances = pdist(black_indices)
distance_matrix = squareform(distances)

optimized_path = solve_tsp(distance_matrix)

optimized_path_points = [black_indices[x] for x in optimized_path]

plt.figure(figsize=(4, 4), dpi=100)
#plt.plot([x[1] for x in optimized_path_points], [x[0] for x in optimized_path_points], color='black', lw=1)
plt.xlim(0, 160)
plt.ylim(0, 160)
plt.gca().invert_yaxis()
plt.xticks([])
plt.yticks([])

plt.axis('off')

#for z in optimized_path_points:
#    print(z)

plt.savefig('traveling-salesman-portrait.png', bbox_inches='tight')

im = Image.open("traveling-salesman-portrait.png")
pix = im.load()

for y in range(len(optimized_path_points)):
    pix[optimized_path_points[y][1], optimized_path_points[y][0]] = (0, 0, 255)

listRelative = []

listRelative.append("S")

count = 1

while(count < len(optimized_path_points)):
    newX = optimized_path_points[count][1] - optimized_path_points[count-1][1]
    newY = optimized_path_points[count][0] - optimized_path_points[count-1][0]
    
    if((newX == 1) and (newY <= 1 and newY >= -1)):
        if(newY == 1):
            #listRelative.append("C")
            listRelative.append("R")
            listRelative.append("D")
        elif(newY == -1):
            #listRelative.append("E")
            listRelative.append("R")
            listRelative.append("U")
        else:
            #if(listRelative[len(listRelative) - 1] == "D"):
            #    listRelative[len(listRelative) - 1] = "C"
            #elif(listRelative[len(listRelative) - 1] == "U"):
            #    listRelative[len(listRelative) - 1] = "E"
            #else:
                listRelative.append("R")
    elif((newX == -1) and (newY <= 1 and newY >= -1)):
        if(newY == 1):
            #listRelative.append("Z")
            listRelative.append("L")
            listRelative.append("D")
        elif(newY == -1):
            #listRelative.append("Q")
            listRelative.append("L")
            listRelative.append("U")
        else:
            #if(listRelative[len(listRelative) - 1] == "D"):
            #    listRelative[len(listRelative) - 1] = "Z"
            #elif(listRelative[len(listRelative) - 1] == "U"):
            #     listRelative[len(listRelative) - 1] = "Q"
            #else:
                listRelative.append("L")
    elif((newY == 1) and newX == 0):
        listRelative.append("D")
    elif((newY == -1) and newX == 0):
        listRelative.append("U")
    else:
        pixelX = optimized_path_points[count-1][1]
        pixelY = optimized_path_points[count-1][0]
        if newX > 0:
            for dif in range(optimized_path_points[count-1][1], optimized_path_points[count][1] + 1):
                listRelative.append("R")
                pix[pixelX, pixelY] = (255, 0, 0)
                pixelX += 1
        else:
            for dif in range(optimized_path_points[count-1][1], optimized_path_points[count][1] - 1, -1):
                listRelative.append("L")
                pix[pixelX, pixelY] = (255, 0, 0)
                pixelX -= 1
                
        if newY > 0:
            for dif in range(optimized_path_points[count-1][0], optimized_path_points[count][0] + 1):
                listRelative.append("D")
                pix[pixelX, pixelY] = (255, 0, 0)
                pixelY += 1
        else:
            for dif in range(optimized_path_points[count-1][0], optimized_path_points[count][0] - 1, -1):
                listRelative.append("U")
                pix[pixelX, pixelY] = (255, 0, 0)
                pixelY -= 1
        
    count = count + 1
    

pix[optimized_path_points[0][1], optimized_path_points[0][0]] = (0, 255, 0)
pix[optimized_path_points[len(optimized_path_points) - 1][1], optimized_path_points[len(optimized_path_points) - 1][0]] = (255, 0, 255)

im.save("traveling-salesman-portrait.png")


print("moves: " + str(len(listRelative)))

image2 = skimage.io.imread('traveling-salesman-portrait.png')
viewer = skimage.viewer.ImageViewer(image2)
viewer.show()

print("Sending path to arduino...")

arduino = serial.Serial('COM3', 115200, write_timeout=1)
sleep(3)

i = 0
restart = "P"

for i in range(1, int(len(listRelative) / 1000) + 1):
    print("Path " + str(i))
    for x in range(1000 * (i - 1), 1000 * i):
        arduino.write(listRelative[x].encode())
        sleep(0.15)
    print("Sending next path...")   
    arduino.write(restart.encode())
    arduino.close()
    sleep(3)
    arduino = serial.Serial('COM3', 115200, write_timeout=1)
    sleep(3)
    
print("Final Path")    
    
for x in range(i * 1000, (i * 1000) + (len(listRelative) % 1000)):
    arduino.write(listRelative[x].encode())
    sleep(0.15)
    

#for x in listRelative:
#   arduino.write(x.encode())
#   sleep(0.15)

print("Done!")
arduino.close()
