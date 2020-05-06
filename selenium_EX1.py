#python + selenium 实现图片对比功能
from selenium import webdriver
from PIL import Image
import unittest
import time 

class ImageCompare(object):
    '''
    实现了对两张图片通过像素比对的算法，获取文件的像素个数大小
    并计算比对结果的相似度的百分比
    '''
    def make_regalur_image(self,img,size=(256,256)):
        # 将图片尺寸强制重置为指定的size大小
        # 然后再将其转换成RGB值
        return img.resize(size).convert('RGB')
    
    def split_image(self,img,part_size=(64,64)):
        #图片切分
        w,h = img.size
        pw,ph = part_size
        #断言是否整除
        return [img.crop((i,j,i+pw,j+ph)).copy()\
                     for i in range(0,w,pw) for j in range(0,h,ph)]
    
    def hist_similar(self,lh,rh):
        #统计切分后每部分图片的相似度频率曲线
        assert len(lh) == len(rh)
        #abs() 函数返回数字的绝对值。
        #max() 方法返回给定参数的最大值，参数可以为序列。
        #zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
        return sum(1 - (0 if l == r else float(abs(l - r)) / max(l,r)) \
                  for l,r in zip(lh,rh)) / len(lh)

    def calc_similar(self,li,ri):
        #计算两张图片相似度
        #histogram()返回一个图像的直方图。这个直方图是关于像素数量的list，图像中的每个象素值对应一个成员。
        return sum(self.hist_similar(l.histogram(),r.histogram()) \
            for l,r in zip(self.split_image(li),self.split_image(ri)))
    
    def calc_similar_by_path(self,lf,rf):
        #使用PIL打开图片
        li,ri = self.make_regalur_image(Image.open(lf)),self.make_regalur_image(Image.open(rf))
        return self.calc_similar(li,ri)

#selenium截取网页图片
class TestDemo(unittest.TestCase):

    def setUp(self):
        #调用图片处理类
        self.IC = ImageCompare()
        #启动浏览器
        self.driver = webdriver.Chrome()

    def test_ImageComparison(self):
        url = "https://www.baidu.com"
        #第一次截图
        self.driver.get(url)
        #self.driver.maximize_window()
        time.sleep(3)
        self.driver.save_screenshot("1.png")
        #第二次截图
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(3)
        self.driver.save_screenshot("2.png")

        # 打印两张截图比对后相似度，100表示完全匹配
        print (self.IC.calc_similar_by_path('1.png','2.png') * 100)

    def close(self):
        #t退出浏览器
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()