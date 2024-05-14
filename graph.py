from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
"""
image = Image.open("3.bmp")
S = np.array(image)
Red = [S[i][j][0] for i in range(len(S)) for j in range(len(S[0]))]
fig, ax = plt.subplots(figsize=(16,10), layout = "constrained")
n, bins, patches = ax.hist(Red, range(min(Red), max(Red)), facecolor = 'darkred', alpha = 0.75)
ax.set_xlabel("Значение красного цвета в RGB")
ax.set_ylabel("Частота данного значения среди пикселей изображения")
ax.set_title("Значения красного для изображения 3.bmp")
ax.grid(True)
plt.savefig("gr3.jpg")

image = Image.open("3_big.bmp")
S = np.array(image)
Red = [S[i][j][0] for i in range(len(S)) for j in range(len(S[0]))]
fig, ax = plt.subplots(figsize=(16,10), layout = "constrained")
n, bins, patches = ax.hist(Red, range(min(Red), max(Red)), facecolor = 'darkred', alpha = 0.75)
ax.set_xlabel("Значение красного цвета в RGB")
ax.set_ylabel("Частота данного значения среди пикселей изображения")
ax.set_title("Значения красного для изображения 3_big.bmp")
ax.grid(True)
plt.savefig("gr3_big.jpg")

image = Image.open("3_new.bmp")
S = np.array(image)
Red = [S[i][j][0] for i in range(len(S)) for j in range(len(S[0]))]
fig, ax = plt.subplots(figsize=(16,10), layout = "constrained")
n, bins, patches = ax.hist(Red, range(min(Red), max(Red)), facecolor = 'darkred', alpha = 0.75)
ax.set_xlabel("Значение красного цвета в RGB")
ax.set_ylabel("Частота данного значения среди пикселей изображения")
ax.set_title("Значения красного для изображения 3_new.bmp")
ax.grid(True)
plt.savefig("gr3_new.jpg")

"""

image1 = Image.open("3_big.bmp")
S1 = np.array(image1)
Red1 = [S1[i][j][0] for i in range(len(S1)) for j in range(len(S1[0]))]

image2 = Image.open("3_new.bmp")
S2 = np.array(image2)
Red2 = [S2[i][j][0] for i in range(len(S2)) for j in range(len(S2[0]))]

fig, ax = plt.subplots(figsize=(16,10), layout = "constrained")

ax.hist(Red1, range(min(Red1), max(Red1)), facecolor = 'red', alpha = 0.5, label='3_big.bmp')
ax.hist(Red2, range(min(Red2), max(Red2)), facecolor = 'blue', alpha = 0.5, label='3_new.bmp')

# Set the labels and title
ax.set_xlabel("Значение красного цвета в RGB")
ax.set_ylabel("Частота данного значения среди пикселей изображения")
ax.set_title("Значения красного для изображений 3_big.bmp и 3_new.bmp")
ax.legend()
ax.grid(True)

# Save the figure
plt.savefig("gr3_both.png")