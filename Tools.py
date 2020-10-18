import cv2
import math
import numpy as np

class autoFocus:

    def __init__(self, _name):
        self.name = _name
        self.imgPath = './img/H&A/'
        # For test focus function
        # self.imgPath = './img/BLS/' + self.name
        self.img = cv2.imread(self.name)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # print(type(self.img))


    def getImgVarLaplacian(self):
        imgVar = cv2.Laplacian(self.img, cv2.CV_64FC4).var()
        print('Laplacian score: ', imgVar)
        return round(imgVar,2)

    def getImgVarTenengrad(self):
        imgVar = cv2.Sobel(self.img, cv2.CV_64F, 2, 1).var()
        print('Sobel score: ', imgVar)
        return round(imgVar, 2)

    def SMD(self):
        '''
        :param img:narray 二维灰度图像
        :return: float 图像约清晰越大
        '''
        shape = np.shape(self.img)
        out = 0
        for x in range(0, shape[0] - 1):
            for y in range(1, shape[1]):
                out += math.fabs(int(self.img[x, y]) - int(self.img[x, y - 1]))
            out += math.fabs(int(self.img[x, y] - int(self.img[x + 1, y])))
        print(out)
        return out

    def brenner(self):
        '''
        :param img:narray 二维灰度图像
        :return: float 图像约清晰越大
        '''
        shape = np.shape(self.img)
        out = 0
        for x in range(0, shape[0] - 2):
            for y in range(0, shape[1]):
                out += (int(self.img[x + 2, y]) - int(self.img[x, y])) ** 2
        print(out)
        return out

    def SMD2(self):
        '''
        :param img:narray 二维灰度图像
        :return: float 图像约清晰越大
        '''
        shape = np.shape(self.img)
        out = 0
        for x in range(0, shape[0] - 1):
            for y in range(0, shape[1] - 1):
                out += math.fabs(int(self.img[x, y]) - int(self.img[x + 1, y])) * math.fabs(int(self.img[x, y] - int(self.img[x, y + 1])))
        print(out)
        return out

    def energy(self):
        '''
        :param img:narray 二维灰度图像
        :return: float 图像约清晰越大
        '''
        shape = np.shape(self.img)
        out = 0
        for x in range(0, shape[0] - 1):
            for y in range(0, shape[1] - 1):
                out += ((int(self.img[x + 1, y]) - int(self.img[x, y])) ** 2) + ((int(self.img[x, y + 1] - int(self.img[x, y]))) ** 2)
        print(out)
        return out

    def variance(self):
        '''
        :param img:narray 二维灰度图像
        :return: float 图像约清晰越大
        '''
        out = 0
        u = np.mean(self.img)
        shape = np.shape(self.img)
        for x in range(0, shape[0]):
            for y in range(0, shape[1]):
                out += (self.img[x, y] - u) ** 2
        print(out)
        return out

    def Vollath(self):
        '''
        :param img:narray 二维灰度图像
        :return: float 图像约清晰越大
        '''
        shape = np.shape(self.img)
        u = np.mean(self.img)
        out = -shape[0] * shape[1] * (u ** 2)
        for x in range(0, shape[0] - 1):
            for y in range(0, shape[1]):
                out += int(self.img[x, y]) * int(self.img[x + 1, y])
        print(out)
        return out

    def entropy(self):
        '''
        :param img:narray 二维灰度图像
        :return: float 图像约清晰越大
        '''
        out = 0
        count = np.shape(self.img)[0] * np.shape(self.img)[1]
        p = np.bincount(np.array(self.img).flatten())
        for i in range(0, len(p)):
            if p[i] != 0:
                out -= p[i] * math.log(p[i] / count) / count
        print('entropy score: ', out)
        return out


if __name__== '__main__':
    autoFocus('1.PNG').getImgVarTenengrad()
    autoFocus('2.PNG').getImgVarTenengrad()
    autoFocus('3.PNG').getImgVarTenengrad()
    autoFocus('4.PNG').getImgVarTenengrad()
    print('---------------------------------')
    autoFocus('1.PNG').entropy()
    autoFocus('2.PNG').entropy()
    autoFocus('3.PNG').entropy()
    autoFocus('4.PNG').entropy()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
