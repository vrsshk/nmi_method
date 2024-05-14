from PIL import Image
import numpy as np
import math
from nmi import*

def MSE(image1, image2):
    c = 0
    width, height = image1.size
    P = np.array(image1).astype(float)
    S = np.array(image2).astype(float)
    for i in range (height):
        for j in range (width):
            c += (P[i][j][0] - S[i][j][0]) ** 2
    mse = c / (width * height)
    return mse

def RMSE(image1, image2):
    mse = MSE(image1, image2)
    rmse = math.sqrt(mse)
    return rmse

def PSNR(image1, image2):
    mse = MSE(image1, image2)
    psnr = 10*math.log10(255**2/mse)
    return psnr

def SSIM(image1, image2):
    K1 = (0.01 * 255)**2
    K2 = (0.03 * 255)**2
    width, height = image1.size
    P = np.array(image1).astype(float)
    S = np.array(image2).astype(float)

    #Вычисляю средние значения
    p_sum = np.sum(P)
    s_sum = np.sum(S)
    p_mean = p_sum / (width * height)
    s_mean = s_sum / (width * height)

    #Вычисляю дисперсии и ковариацию
    p_deviation_sum = np.sum((P - p_mean)**2)
    s_deviation_sum = np.sum((S - s_mean)**2)
    ps_deviation_sum = np.sum((P - p_mean)*(S - s_mean))
    p_variance = p_deviation_sum / (width * height)
    s_variance = s_deviation_sum / (width * height)
    ps_covariance = ps_deviation_sum / (width * height)

    #Вычисляю метрику
    numerator = (2*p_mean*s_mean + K1)*(2*ps_covariance + K2)
    denominator = (p_mean**2 + s_mean**2 + K1)*(p_variance + s_variance + K2)
    ssim = numerator/denominator
    return ssim

def size(image: Image):
    """Длина максимально возможного сообщения

    Args:
        image (Image): Изображение
    Returns:
        float: Максимальная длина сообщения для встраивания
    """
    size = 0
    #буду работать в красном цвете, k = 0
    p_image = interpolation(image)
    width, height = image.size
    P = np.array(p_image)

    #проход по блокам 2 х 2
    for i in range (height):
        for j in range (width):

            Pd = int(P[2*i][2*j][0]) #основной пиксель 

            for x, y in [(2*i, 2*j + 1), (2*i + 1, 2*j), (2*i + 1, 2*j + 1)]:
                d = abs(int(P[x][y][0]) - Pd)
                if (d == 0 or d ==1):
                    continue
                n = int(math.log2(d))
                size +=n
    size = size // 8
    return(size)

