from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

#主程序
def main():
    url = "http://www.mangabz.com/"
    driver = webdriver.Chrome()
    #restul = scroll_screenshot(url,driver)
    #print(restul)
    data = find_elem(url,driver)
    print(data)


#元素定位
'''
find_element_by_id   通过 ID 查找元素，也就是检查元素里的 id 属性
find_element_by_name    通过查找名字的方式，对元素进行定位。检查元素中的name属性
find_element_by_xpath  通过查找元素的路径去查找元素 copy Xpath
find_element_by_link_text  通过查找页面的文本信息进行定位
find_element_by_partial_link_text  通过模糊文本信息查找元素
find_element_by_tag_name  通过元素的标签属性对元素进行定位
find_element_by_class_name  通过查找 class_name 的方式对元素进行定位，检查属性中的class属性
find_element_by_css_selector  通过查找元素的路径去查找元素 copy selector

返回列表
find_elements_by_name --- find_elements_by_css_selector
'''
def find_elem(url,driver):
    driver.get(url)

    print(driver.title) #标题
    search = driver.find_element_by_id("txtKeywords")  #寻找搜索框
    search.clear()  #清空值
    search.send_keys("虫师")   #输入数据
    driver.find_element_by_id("btnSearch").click()  #点击搜索
    time.sleep(2)

    #因为搜索跳转到了新标签，所以需要返回主页
    handles = driver.window_handles  #获得所有句柄
    driver.switch_to.window(handles[0])  #切换到旧标签
 
    #Mosted_elem = driver.find_element_by_class_name("list-con-1")
    #定位所有所需a标签
    Mosted_all = driver.find_elements_by_xpath("//div[@class='list-con-1']/div[@class='index-manga-list']/div[@class='index-manga-item']/p[@class='index-manga-item-title']/a")
    #Mosted_all = Mosted_elem.find_elements_by_css_selector("div.list-con-1 > div > div > p.index-manga-item-title > a")
    Mosted = []
    for M in Mosted_all:
        Mosted.append(M.text)  #提取标签文本
    
    #print(Mosted_elem.get_attribute('innerHTML'))   #源码

    Hot_all = driver.find_elements_by_css_selector("div.rank-con > div > div > p.rank-item-title > a")
    Hot = []
    for H in Hot_all:
        Hot.append(H.text)
    
    Editer_all = driver.find_elements_by_css_selector("div.list-con-2 > div > div > div > div:nth-child(2) > div > p.index-manga-item-title > a")
    Editer = []
    for E in Editer_all:
        Editer.append(E.text)

    Up_all = driver.find_elements_by_css_selector("body > div:nth-child(6) > div > div > div.carousel-right-list > div > p.carousel-right-item-title > a")
    Up = []
    for U in Up_all:
        Up.append(U.text)

    #需要鼠标悬停在指定位置才显示内容，可用ActionChains模拟鼠标
    Popular_categories = []
    actions = ActionChains(driver) 
    Warm = driver.find_element_by_xpath("//*[@id='hotCatgoryId']/p/span[2]/a[1]")
    Love = driver.find_element_by_xpath("//*[@id='hotCatgoryId']/p/span[2]/a[2]")
    Campus = driver.find_element_by_xpath("//*[@id='hotCatgoryId']/p/span[2]/a[3]")
    Fantasy = driver.find_element_by_xpath("//*[@id='hotCatgoryId']/p/span[2]/a[4]")
    Science = driver.find_element_by_xpath("//*[@id='hotCatgoryId']/p/span[2]/a[5]")
    #鼠标移动到elem
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    actions.move_to_element(Warm).perform()
    Warm_all = driver.find_elements_by_xpath("//*[@id='hotCatgoryId']/div[1]/div/p[1]/a")
    for P in Warm_all:
        Popular_categories.append(P.text)
    time.sleep(2)
    actions.move_to_element(Love).perform()
    Love_all = driver.find_elements_by_xpath("//*[@id='hotCatgoryId']/div[2]/div/p[1]/a")
    for P in Love_all:
        Popular_categories.append(P.text)
    time.sleep(2)
    actions.move_to_element(Campus).perform()
    Campus_all = driver.find_elements_by_xpath("//*[@id='hotCatgoryId']/div[3]/div/p[1]/a")
    for P in Campus_all:
        Popular_categories.append(P.text)
    time.sleep(2)
    actions.move_to_element(Fantasy).perform()
    Fantasy_all = driver.find_elements_by_xpath("//*[@id='hotCatgoryId']/div[4]/div/p[1]/a")
    for P in Fantasy_all:
        Popular_categories.append(P.text)
    time.sleep(2)
    actions.move_to_element(Science).perform()
    Science_all = driver.find_elements_by_xpath("//*[@id='hotCatgoryId']/div[5]/div/p[1]/a")
    for P in Science_all:
        Popular_categories.append(P.text)
    time.sleep(2)
    #Popular_categories_all = Warm_all + Love_all + Campus_all + Fantasy_all + Science_all
    #for P in Popular_categories_all:
        #Popular_categories.append(P.text)


    data = { "人氣推薦":Mosted,"热度排行":Hot,"編輯推薦":Editer,"上升最快":Up,"熱門分類":Popular_categories }
   
    return data


#滚动和截图
def scroll_screenshot(url,driver):
    driver.get(url)
    driver.maximize_window() #窗口最大化
    driver.save_screenshot("top.png")  #截图
    #execute_script 为执行js代码
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #滚动到底部  scrollTo(xpos,ypos)
    driver.save_screenshot("bottom.png")
    
    time.sleep(5)
    return "ok"

#鼠标操作
'''
    action.click();  // 鼠标左键在当前停留的位置做单击操作
    action.contextClick();  //鼠标右键在当前停留的位置做单击操作
    action.doubleClick();  //鼠标在当前停留位置做双击操作
    action.dragAndDrop(source,target);  //将 source 元素拖放到 target 元素的位置
    action.clickAndHold();   // 鼠标悬停在当前位置，既点击并且不释放
    action.moveToElement(toElement);   // 将鼠标移到 toElement 元素中点
    action.release();   //释放鼠标
'''

def drag_and_drop():

    browser = webdriver.Chrome()
    url = "http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable"
    browser.get(url)
    browser.switch_to.frame('iframeResult')
    source = browser.find_element_by_css_selector('#draggable')
    target = browser.find_element_by_css_selector('#droppable')
    actions = ActionChains(browser)
    actions.drag_and_drop(source, target)
    actions.perform()


if __name__ == "__main__":
    main()




