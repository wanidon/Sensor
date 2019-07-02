#-coding:utf-8-
'''
This code binarizes the given image to black and white by otsu's method.
This can run with python3 and python2.
大津の手法により、与えられた画像を白黒に二値化します。
python2でもpython3でも動作します。

if you gives 'foo.png', this outputs 'foo_bin.png'.
'hoge.jpg'を与えた場合、'hoge_bin.jpg'を出力します。
'''
from PIL import Image
import numpy as np

def binarize(IMAGEPATH):

    with Image.open(IMAGEPATH) as img:
        img = np.array(img.convert('L')) #convert to grayscale, グレイスケールに変換


    #brightness value histogram, 輝度値ヒストグラム
    hist = [0] * 256 
    for i in range(len(img)):
        for j in range(len(img[0])):
            hist[img[i][j]] = hist[img[i][j]] + 1


    numB = 0                    #number of black class pixels, 黒クラスの画素の数
    numW = len(img)*len(img[0]) #number of white class pixels, 白クラスの画素の数
    maxV = 0 #numerator of between-class variance, クラス間分散の分子
    t    = 0 #threshold, しきい値

    #find t which maximizes maxV, maxVを最大化するtを探索
    for i in range(1,256): #from 1 to 255
        numB = numB + hist[i-1] 
        numW = numW - hist[i-1]
        if numB == 0 or numW == 0:
            continue
        meanB = np.dot(hist[:i],np.array(range(256))[:i]) / numB #mean brightness value of black class, 黒クラスの平均輝度値
        meanW = np.dot(hist[i:],np.array(range(256))[i:]) / numW #mean brightness value of white class, 白クラスの平均輝度値
        v = numB * numW * (meanB-meanW)**2

        if maxV < v:
            maxV = v
            t = i

    #binarization, 二値化
    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j] = 0 if img[i][j] < t else 255
    
    img = Image.fromarray(np.uint8(img))
    img.save(IMAGEPATH.split('.')[0]+"_bin."+IMAGEPATH.split('.')[1])
