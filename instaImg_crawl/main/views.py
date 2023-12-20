import base64

from django.shortcuts import render
from django.http import JsonResponse
from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.shortcuts import render, redirect
import time
import os
from django.http import Http404
from base64 import b64encode
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Photo1, CustomUser
from django.http import HttpResponse
import requests  # requests 모듈을 임포트
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main:login')
    template_name = 'registration/signup.html'

def index(request):
    return render(request, 'main/index.html')

def main(request):
    return render(request, 'registration/main.html')

def client(request):

    return render(request, 'main/client.html')

def proxy_instagram_image(request, image_url):
    try:
        # Instagram 이미지에 대한 요청을 수행
        response = requests.get(image_url)

        # 응답을 그대로 클라이언트에게 전달
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    except Exception as e:
        return HttpResponse(str(e), status=500)
def find_id(request):
    return render(request, 'main/find_id.html')

def find_pw(request):
    return render(request, 'main/find_pw.html')

def adminwindow(request):
    # admin 페이지의 내용을 처리하는 코드 추가
    return render(request, 'main/adminwindow.html')  # 예시로 'main/admin.html'로 렌더링하도록 설정

def find_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        try:
            # 변경된 컬럼명에 맞게 수정
            user = CustomUser.objects.get(first_name=first_name, last_name=last_name, email=email)
            return JsonResponse({'found': True, 'username': user.username})
        except CustomUser.DoesNotExist:
            return JsonResponse({'found': False})

    return render(request, 'find_id.html')

def find_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        try:
            # 변경된 컬럼명에 맞게 수정
            user = CustomUser.objects.get(username=username, first_name=first_name, last_name=last_name, email=email)
            return JsonResponse({'found': True, 'password': user.password})
        except CustomUser.DoesNotExist:
            return JsonResponse({'found': False})

    return render(request, 'find_pw.html')

@csrf_exempt
def get_image_url(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        photo = Photo1.objects.filter(keyword=keyword).first()

        if photo:
            return JsonResponse({'image_url': photo.image_src})
        else:
            return JsonResponse({'error': 'Image not found for the given keyword'}, status=404)
def get_photos(request):
    photos = Photo1.objects.all().values('keyword', 'image_src')
    return JsonResponse(list(photos), safe=False)
def detail_img(request):
    baseUrl = 'https://www.instagram.com/explore/tags/'
    plusUrl = request.GET.get('account')
    plusUrl = str(plusUrl)
    url = baseUrl + quote_plus(plusUrl)

    save_folder = os.path.join(r'C:/Users/user/PycharmProjects/instaImg_crawl/instaImg_crawl/img/', plusUrl)
    os.makedirs(save_folder, exist_ok=True)

    # 크롬 드라이버 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 화면 최소화 옵션 추가
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\user\PycharmProjects\instaImg_crawl\instaImg_crawl\chromedriver.exe',
        options=chrome_options
    )

    driver.get(url)

    pageDown = 10
    while pageDown:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        pageDown -= 1

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

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
        posts.update({img: text})

    insta = soup.select('._aabd._aa8k._al3l')

    n = 1
    for i in insta:
        imgUrl = i.select_one('._aagv').img['src']
        img_path = os.path.join(save_folder, f'{plusUrl}{n}.jpg')

        with urlopen(imgUrl) as f:
            with open(img_path, 'wb') as h:
                img = f.read()
                h.write(img)
            n += 1

    driver.close()

    # 폴더 내의 이미지 목록 가져오기
    folderImagePaths = [os.path.join(save_folder, f'{plusUrl}{i}.jpg') for i in range(1, n)]

    # 이미지를 Base64로 변환하여 리스트에 추가
    base64_images = []
    for img_path in folderImagePaths:
        with open(img_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_images.append(base64_image)

    # JSON 응답으로 이미지 목록 전송
    return JsonResponse({'image_list': base64_images})


def folder_list(request):
    folder_path = r'C:/Users/user/PycharmProjects/instaImg_crawl/instaImg_crawl/img/'
    folder_names = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    return render(request, 'main/folder_list.html', {'folder_names': folder_names})


def show_folder_images(request, folder_name):
    folder_path = f'C:/Users/user/PycharmProjects/instaImg_crawl/instaImg_crawl/img/{folder_name}/'
    if not os.path.exists(folder_path):
        raise Http404("Folder does not exist")
    image_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            with open(f'{folder_path}/{filename}', "rb") as image_file:
                encoded_string = b64encode(image_file.read()).decode('utf-8')
                image_list.append(encoded_string)
    return render(request, 'main/show_folder_images.html', {'folder_name': folder_name, 'image_list': image_list})