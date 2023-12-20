# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_folder = models.CharField(max_length=255, blank=True, null=True)

class YourImageModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    search_term = models.CharField(max_length=255)
    image_url = models.URLField()
    additional_info = models.TextField()

    def __str__(self):
        return f"{self.search_term} - {self.image_url}"

    class Meta:
        db_table = 'img'  # 여기에 특정한 테이블 이름을 지정할 수 있습니다.


class Photo1(models.Model):
    id = models.BigAutoField(primary_key=True)
    keyword = models.CharField(max_length=255)
    image_src = models.TextField(null=True)

class UserImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    image_url = models.URLField()
    additional_info = models.TextField()

    def __str__(self):
        return f"{self.keyword} - {self.image_url}"

    class Meta:
        db_table = 'user_image'

