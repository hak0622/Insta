from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager



baseUrl = 'https://gramtower.com/profile/'
plusUrl = '2272buk'
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Firefox(executable_path='/Users/kimbyeonguk/Desktop/practice/django/instaPrj/geckodriver')
driver.get(url)


html = driver.page_source
soup = BeautifulSoup(html)
html = driver.page_source
soup = BeautifulSoup(html)

instaImg = soup.select('div.grid-item>div>a')
instaText = soup.select('div.grid-item>div.p-4>div.break-words')

imgSrcList = []
textList = []
posts = {}

for i in instaImg:
    imgSrcList.append(i.img['src'])

for i in instaText:
    textList.append(i)

for i in range(len(imgSrcList)):
    img = imgSrcList[i]
    text = textList[i]
    posts.update({img:text})

for key,value in posts.items():
    print(key)
    print(value)


driver.close()



'''
baseUrl = 'https://gramtower.com/profile/'
plusUrl = '2272buk'
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome('./chromedriver')
driver.get(url)



html = driver.page_source
soup = BeautifulSoup(html)

instaImg = soup.select('div.grid-item>div>a')
instaText = soup.select('div.grid-item>div.p-4>div.break-words')


imgSrcList = []
textList = []

for i in instaImg:
    imgSrcList.append(i.img['src'])

for i in instaText:
    textList.append(i)


print(imgSrcList)
print(textList)

driver.close()
'''

'''
baseUrl = 'https://bigsta.net/account/'
plusUrl = '2272buk'
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome('./chromedriver')
driver.get(url)

pageDown = 20
while pageDown:
    try:
        driver.find_element_by_class_name("some-loadMore").click()
        time.sleep(1)
    except:
        pass
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        pageDown -= 1



html = driver.page_source
soup = BeautifulSoup(html)

insta = soup.select('figure')

imgSrcList = []

for i in insta:
    imgSrcList.append(i.img['src'])

print(imgSrcList)
driver.close()

return render(request,'main/index.html',{'imgSrcList':imgSrcList})

'''
