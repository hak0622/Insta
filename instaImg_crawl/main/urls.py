# main/urls.py


from . import views

from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import SignUpView, get_photos,get_image_url,proxy_instagram_image

app_name = 'main'

urlpatterns = [
    path('', views.main, name='main'), # 추가된 부분
    path('adminwindow/', views.adminwindow, name='adminwindow'),  # admin 패턴 추가
    path('index/', views.index, name='index'),
    path('detail_img/', views.detail_img, name='detail_img'),
    path('folder_list/', views.folder_list, name='folder_list'),  # 이름을 'folder_list'로 지정
    #path('show_folder_images/<str:folder_name>/', views.show_folder_images, name='show_folder_images'),
    path('client/', views.client, name='client'),
    path('folder_list/<str:folder_name>/', views.show_folder_images, name='show_folder_images'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('find_id/', views.find_id, name='find_id'),
    path('find_user/', views.find_user, name='find_user'),
    path('find_pw/', views.find_pw, name='find_pw'),
    path('find_password/', views.find_password, name='find_password'),
    path('get_photos/', get_photos, name='get_photos'),
    path('api/get-photos/', get_photos, name='get_photos'),
    path('api/get-image-url/', get_image_url, name='get_image_url'),
    path('api/proxy-instagram-image/<path:image_url>/', proxy_instagram_image, name='proxy_instagram_image'),

]