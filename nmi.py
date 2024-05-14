from PIL import Image
import numpy as np
import math

def str_to_bitstring(s: str) -> str:
    """
    Исходная строка преобразуется в строку бит

    Args:
        s (str): Исходная текстовая строка

    Returns:
        str: Строка из нулей и единиц
    """

    bitstring = ''.join(format(ord(c), '08b') for c in s)
    return bitstring

def bitstring_to_str(bitstring: str) -> str:
    """
    Строка бит преобразуется в текстовую строку

    Args:
        s (str): Строка из нулей и единиц

    Returns:
        str: Текстовая строка
    """
    byte_strings = [bitstring[i:i + 8] for i in range(0, len(bitstring), 8)]
    string = ''.join(chr(int(bs, 2)) for bs in byte_strings)
    return string

def interpolation(image: Image) -> Image:
    """
    Исходное изображение m x n преобразуется в изображение 2m x 2n с помощью интерполяции

    Args:
        image (Image): Оригинальное изображение
    
    Returns:
        Image: Увеличенное изображение
    """
    width, height = image.size
    C = np.array(image)
    P = np.zeros((height*2 , width*2, 3))
    #Переношу в большое изображение старые пиксели
    for i in range (height):
        for j in range (width):
            for k in range (3):
                P[2*i][2*j][k] = C[i][j][k]
    #Генерирую новые пиксели
    for i in range(2*height - 1):
        for j in range(2*width - 1):
            if (i%2 == 0 and j%2 == 1):
                for k in range(3):
                    P[i][j][k] = int((P[i][j-1][k] + P[i][j+1][k])/2)
            elif(i%2 == 1 and j%2 == 0):
                for k in range(3):
                    P[i][j][k] = int((P[i- 1][j][k] + P[i+1][j][k])/2)
            elif(i%2 == 1 and j%2 == 1):
                for k in range(3):
                    P[i][j][k] = int((P[i - 1][j - 1][k] + P[i - 1][j][k] + P[i][j - 1][k])/3)
    #Генерирую новые пиксели для краевых участков
    for i in range(2*height - 1):
        for k in range(3):
                    P[i][-1][k] = int((P[i][-2][k] + P[i][-3][k])/2)
    for j in range(2*width - 1):
        for k in range(3):
                    P[-1][j][k] = int((P[-2][j][k] + P[-3][j][k])/2)
    for k in range(3):
        P[-1][-1][k] = int((P[-2][-1][k] + P[-1][-2][k] + P[-2][-2][k])/3)

    new_image = Image.fromarray(P.astype('uint8'), 'RGB')
    return(new_image)

def compression(image: Image) -> Image:
    """
    Исходное изображение 2m x 2n преобразуется в изображение m x n

    Args:
        image (Image): Увеличенное изображение

    Returns:
        Image: Сжатое изображение
    """
    width, height = image.size
    P = np.array(image)
    C = np.zeros((height//2 , width//2, 3))
    for i in range (height//2):
        for j in range (width//2):
            for k in range (3):
                C[i][j][k] = P[2*i][2*j][k]
    new_image = Image.fromarray(C.astype('uint8'), 'RGB')
    return new_image

def encode(image: Image, message: str) -> Image:
    """Встраивание информации в изображение,  метод Neighbor Mean Interpolation

    Args:
        image (Image): Изображение
        message (_type_): Сообщение, которое необходимо встроить
    Returns:
        Image: Стегаизображение
    """
    bitstring = str_to_bitstring(message)
    #буду работать в красном цвете, k = 0
    p_image = interpolation(image)
    width, height = image.size
    P = np.array(p_image)

    #проход по блокам 2 х 2
    break_flag = False
    for i in range (height):
        for j in range (width):

            Pd = int(P[2*i][2*j][0]) #основной пиксель 

            for x, y in [(2*i, 2*j + 1), (2*i + 1, 2*j), (2*i + 1, 2*j + 1)]:
                d = abs(int(P[x][y][0]) - Pd)
                if (d == 0 or d ==1):
                    continue
                n = int(math.log2(d))

                if (len(bitstring) == 0):
                    break_flag = True
                    break
                elif (len(bitstring) < n):
                    m = int(bitstring, 2)
                    P[x][y][0] += m
                    bitstring = ""
                    break
                else:
                    m = int(bitstring[-n:], 2)
                    P[x][y][0] += m
                    bitstring = bitstring[0 : -n]

            if break_flag:
                break

        if break_flag:
            break

    s_image = Image.fromarray(P.astype('uint8'), 'RGB') #стегаизображение
    return(s_image)

def decode(s_image:Image) -> str:
    image = compression(s_image)#исходное изображение
    width, height = image.size
    p_image = interpolation(image)#увеличенное изображение
    P = np.array(p_image)
    S = np.array(s_image)

    message = ""
    bitstring = ""
    #проход по блокам 2 х 2
    for i in range (height):
        for j in range (width):
            Pd = int(P[2*i][2*j][0]) #основной пиксель 
            for x, y in [(2*i, 2*j + 1), (2*i + 1, 2*j), (2*i + 1, 2*j + 1)]:
                d = abs(int(P[x][y][0]) - Pd)
                m = abs(S[x][y][0] - P[x][y][0])

                if (d == 0 or d == 1):
                    n = 0
                else:
                    n = int(math.log2(d))
                    bitstring = bin(m)[2:].zfill(n) + bitstring
    #make_multiple_of_8(bitstring)
    while len(bitstring) % 8 != 0:
        bitstring = bitstring[1:]
    message = bitstring_to_str(bitstring)
    return message
