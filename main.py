from PIL import Image
import numpy as np
import math
from nmi import*
from analysis import*

#image = Image.open("2.bmp")
#print(size(image))

choice = input("Для встраивания информации выберите E, для извлечения D:\n")
image_number = int(input("Выберите номер изображения (1-3): \n"))
if choice.upper() == 'E':
    image = Image.open(f"{image_number}.bmp")
    message = input("Введите сообщение для встраивания: \n")
    #with open('long_message.txt') as f:
    #    message = f.read()
    image1 = interpolation(image)
    image1.save(f"{image_number}_big.bmp")
    image2 = encode(image, message)
    image2.save(f"{image_number}_new.bmp")
    print(f"Ваше стегоизображение {image_number}_new.bmp сохранено.\n")
    mse = MSE(image1, image2)
    rmse = RMSE(image1, image2)
    psnr = PSNR(image1, image2)
    ssim = SSIM(image1, image2)
    print(f"Ниже представлены полученные метрики:\n" )
    print("MSE = ", mse, "\n")
    print("RMSE = ", rmse, "\n")
    print("PSNR = ", psnr, "\n")
    print("SSIM = ", ssim, "\n")
elif choice.upper() == 'D':
    new_image = Image.open(f"{image_number}_new.bmp")
    #new_image = Image.open("3_new_1.bmp")
    message = decode(new_image)
    print(f"Из стегоизображения {image_number}_new.bmp был получено сообщение: \n", message)
    print(len(message))
